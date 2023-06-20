import pickle
import os
import uuid
import sys
from pathlib import Path
from datetime import datetime
from dateutil.relativedelta import relativedelta

import pandas as pd
import mlflow
from prefect import flow, task, get_run_logger
from prefect.context import get_run_context

os.environ["AWS_PROFILE"] = "default"


def download_pipeline(run_id: str):
    path = mlflow.artifacts.download_artifacts(
        artifact_uri=f"s3://mlopszoomcamp-alex/1/{run_id}/artifacts/model/model.pkl")

    with open(path, 'rb') as f_out:
        pipeline = pickle.load(f_out)
    return pipeline


def read_dataframe(filename: str):
    df = pd.read_parquet(filename)

    df['duration'] = df.lpep_dropoff_datetime - df.lpep_pickup_datetime
    df.duration = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)]

    df['ride_id'] = [str(uuid.uuid4()) for _ in range(len(df))]

    return df


def prepare_dictionaries(df: pd.DataFrame):
    categorical = ['PULocationID', 'DOLocationID']
    df[categorical] = df[categorical].astype(str)
    df['PU_DO'] = df['PULocationID'] + '_' + df['DOLocationID']
    categorical = ['PU_DO']
    numerical = ['trip_distance']
    return df[categorical + numerical].to_dict(orient='records')


def save_results(df, y_pred, run_id, output_file):
    df_result = pd.DataFrame()
    df_result[['ride_id', 'lpep_pickup_datetime', 'PULocationID', 'DOLocationID']
              ] = df[['ride_id', 'lpep_pickup_datetime', 'PULocationID', 'DOLocationID']]
    df_result['actual_duration'] = df['duration']
    df_result['predicted_duration'] = y_pred

    df_result['diff'] = df_result['actual_duration'] - \
        df_result['predicted_duration']

    df_result['model_version'] = run_id
    df_result.to_parquet(output_file, index=False)


@task
def apply_model(input_file: str, output_file: str, run_id: str) -> None:
    logger = get_run_logger()

    logger.info(f'reading the data from the {input_file}...')
    df = read_dataframe(input_file)
    dicts = prepare_dictionaries(df)

    logger.info(f'loading pipeline with RUN_ID={run_id}...')
    pipeline = download_pipeline(run_id)
    logger.info('applying the model...')
    y_pred = pipeline.predict(dicts)

    logger.info(f'saving the results to {output_file}...')
    save_results(df, y_pred, run_id, output_file)
    return output_file


def get_paths(run_date, taxi_type, run_id):
    prev_month = run_date - relativedelta(months=1)
    year = prev_month.year
    month = prev_month.month

    input_file = f'https://d37ci6vzurychx.cloudfront.net/trip-data/{taxi_type}_tripdata_{year:04d}-{month:02d}.parquet'
    output_file = f's3://mlopszoomcamp-alex/output/{taxi_type}/{year:04d}-{month:02d}-{run_id}.parquet'

    return input_file, output_file


@flow
def ride_duration_prediction(
        taxi_type: str,
        run_id: str,
        run_date: datetime = None):
    if run_date is None:
        ctx = get_run_context()
        run_date = ctx.flow_run.expected_start_time

    input_file, output_file = get_paths(run_date, taxi_type, run_id)

    apply_model(input_file, output_file, run_id)


def run():
    taxi_type = sys.argv[1]  # 'green'
    year = int(sys.argv[2])  # 2021
    month = int(sys.argv[3])  # 3
    RUN_ID = 'a4b217a84e3a44ad870271b75331eb6c'
    # RUN_ID = sys.argv[4]

    ride_duration_prediction(taxi_type=taxi_type,
                             run_id=RUN_ID,
                             run_date=datetime(year=year, month=month, day=1))


if __name__ == '__main__':
    run()
