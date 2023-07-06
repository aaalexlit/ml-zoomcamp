import datetime
import time
import random
import logging
import uuid
import pytz
import pandas as pd
import io
import psycopg
import joblib
from calendar import monthrange

from prefect import task, flow

from evidently import ColumnMapping
from evidently.report import Report
from evidently.metrics import ColumnDriftMetric, DatasetDriftMetric, DatasetMissingValuesMetric
from evidently.metrics import ColumnQuantileMetric, ColumnCorrelationsMetric
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s]: %(message)s")

DB_NAME = "monitoring"

create_table_statement = """
drop table if exists metrics;
create table metrics(
    timestamp timestamptz,
    prediction_drift float,
    num_drifted_columns integer,
    missing_values_share float,
    fare_amount_quantile float,
    fare_amount_trip_dist_spearman_corr float
)
"""
year = 2023
month = 3

reference_data = pd.read_parquet('../data/reference.parquet')

with open("models/lin_reg.bin", "rb") as f_in:
    model = joblib.load(f_in)

data_url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_{year:04d}-{month:02d}.parquet"
raw_data = pd.read_parquet(data_url)

begin = datetime.datetime(year, month, 1, 0, 0)
num_features = ['passenger_count',
                'trip_distance', 'fare_amount', 'total_amount']
cat_features = ['PULocationID', 'DOLocationID']
column_mapping = ColumnMapping(
    prediction='prediction',
    numerical_features=num_features,
    categorical_features=cat_features,
    target=None
)

report = Report(metrics=[
    ColumnDriftMetric(column_name='prediction'),
    DatasetDriftMetric(),
    DatasetMissingValuesMetric(),
    ColumnQuantileMetric(column_name='fare_amount',
                         quantile=0.5),
    ColumnCorrelationsMetric(column_name='fare_amount'),
])


@task(name="prepare the database")
def prep_db():
    with psycopg.connect("host=localhost port=5432 user=postgres password=example", autocommit=True) as conn:
        res = conn.execute(
            f"SELECT 1 FROM pg_database WHERE datname='{DB_NAME}'")
        if len(res.fetchall()) == 0:
            conn.execute("create database monitoring;")
        with psycopg.connect(f"host=localhost port=5432 dbname={DB_NAME} user=postgres password=example") as conn:
            conn.execute(create_table_statement)


@task(retries=2, retry_delay_seconds=5, name="calculate metrics")
def calculate_metrics_postgresql(curr, day_number):
    current_data = raw_data[(raw_data.lpep_pickup_datetime >= (begin + datetime.timedelta(day_number))) &
                            (raw_data.lpep_pickup_datetime < (begin + datetime.timedelta(day_number + 1)))]
    current_data.fillna(0, inplace=True)
    current_data['prediction'] = model.predict(
        current_data[num_features + cat_features])
    report.run(reference_data=reference_data,
               current_data=current_data,
               column_mapping=column_mapping)
    result = report.as_dict()
    prediction_drift = result['metrics'][0]['result']['drift_score']
    num_drifted_columns = result['metrics'][1]['result']['number_of_drifted_columns']
    missing_values_share = result['metrics'][2]['result']['current']['share_of_missing_values']
    fare_amount_quantile_metric = result['metrics'][3]['result']['current']['value']
    fare_amount_trip_dist_spearman_corr = result['metrics'][4]['result']['current']['spearman']['values']['y'][1]
    insert_query = f"""insert into metrics(timestamp, prediction_drift, num_drifted_columns, missing_values_share, fare_amount_quantile, fare_amount_trip_dist_spearman_corr) 
    values ('{begin + datetime.timedelta(day_number)}', 
    {prediction_drift}, '{num_drifted_columns}',{missing_values_share}, {fare_amount_quantile_metric}, {fare_amount_trip_dist_spearman_corr})"""

    curr.execute(insert_query)


@flow
def batch_monitoring_backfill():
    prep_db()
    last_send = datetime.datetime.now()
    with psycopg.connect(f"host=localhost port=5432 dbname={DB_NAME} user=postgres password=example",
                         autocommit=True) as conn:
        num_of_days_in_month = monthrange(year, month)[1]
        for day_number in range(1, num_of_days_in_month):
            with conn.cursor() as curr:
                calculate_metrics_postgresql(curr, day_number=day_number)

if __name__ == '__main__':
    batch_monitoring_backfill()
