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

from prefect import task, flow

from evidently import ColumnMapping
from evidently.report import Report
from evidently.metrics import ColumnDriftMetric, DatasetDriftMetric, DatasetMissingValuesMetric
from evidently.metrics import ColumnQuantileMetric
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s]: %(message)s")

DB_NAME = "monitoring"

SEND_TIMEOUT = 10
rand = random.Random()

create_table_statement = """
drop table if exists metrics;
create table metrics(
    timestamp timestamptz,
    prediction_drift float,
    num_drifted_columns integer,
    missing_values_share float
)
"""

reference_data = pd.read_parquet('../data/reference.parquet')

with open("models/lin_reg.bin", "rb") as f_in:
    model = joblib.load(f_in)

raw_data = pd.read_parquet('../data/green_tripdata_2023-03.parquet')

begin = datetime.datetime(2022, 2, 1, 0, 0)
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
    ColumnQuantileMetric() 

])


@task
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
    insert_query = f"""insert into metrics(timestamp, prediction_drift, num_drifted_columns, missing_values_share) 
    values ('{begin + datetime.timedelta(day_number)}', 
    {prediction_drift}, '{num_drifted_columns}',{missing_values_share})"""

    curr.execute(insert_query)

@flow
def batch_monitoring_backfill():
    prep_db()
    last_send = datetime.datetime.now()
    with psycopg.connect(f"host=localhost port=5432 dbname={DB_NAME} user=postgres password=example",
                         autocommit=True) as conn:
        for day_number in range(27):
            with conn.cursor() as curr:
                calculate_metrics_postgresql(curr, day_number=day_number)

            new_send = datetime.datetime.now()
            seconds_elapsed = (new_send - last_send).total_seconds()
            if seconds_elapsed < SEND_TIMEOUT:
                time.sleep(SEND_TIMEOUT - seconds_elapsed)
            last_send = last_send + datetime.timedelta(seconds=10)
            logging.info("data sent")


if __name__ == '__main__':
    batch_monitoring_backfill()

