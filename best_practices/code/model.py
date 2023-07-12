import json
import os
import pickle
import base64

import boto3
import mlflow


def get_model_uri(run_id):
    model_location = os.getenv('MODEL_LOCATION')

    if model_location is not None:
        return model_location

    model_bucket = os.getenv('MODEL_BUCKET', 'mlopszoomcamp-alex')
    experiment_id = os.getenv('MLFLOW_EXPERIMENT_ID', '1')

    model_location = f"s3://{model_bucket}/{experiment_id}/{run_id}/artifacts/model/model.pkl"
    return model_location


def load_pipeline(run_id: str):
    model_uri = get_model_uri(run_id)
    path = mlflow.artifacts.download_artifacts(
        artifact_uri=model_uri)
    with open(path, 'rb') as f_out:
        return pickle.load(f_out)


def base64_decode(encoded_data):
    decoded_data = base64.b64decode(encoded_data).decode('utf-8')
    return json.loads(decoded_data)


class ModelService:

    def __init__(self, pipeline,
                 model_version=None,
                 callbacks=None):
        self.pipeline = pipeline
        self.model_version = model_version
        self.callbacks = callbacks or []

    def prepare_features(self, ride):
        return {
            'PU_DO': f"{ride['PULocationID']}_{ride['DOLocationID']}",
            'trip_distance': ride['trip_distance'],
        }

    def predict(self, features):
        return self.pipeline.predict(features)[0]

    def lambda_handler(self, event):
        predictions = []
        for record in event['Records']:
            encoded_data = record['kinesis']['data']
            ride_event = base64_decode(encoded_data)
            ride = ride_event['ride']
            ride_id = ride_event['ride_id']

            features = self.prepare_features(ride)
            prediction = self.predict(features)
            prediction_event = {
                'model': 'ride_duration_prediction_model',
                'version': self.model_version,
                'prediction': {
                    'ride_duration': prediction,
                    'ride_id': ride_id
                }
            }

            for callback in self.callbacks:
                callback(prediction_event)

            predictions.append(prediction_event)
        return predictions


class KinesisCallback:

    def __init__(self, kinesis_client, prediction_stream_name):
        self.kinesis_client = create_kinesis_client()
        self.prediction_stream_name = prediction_stream_name

    def put_record(self, prediction_event):
        self.kinesis_client.put_record(
            StreamName=self.prediction_stream_name,
            Data=json.dumps(prediction_event),
            PartitionKey='1',
        )


def create_kinesis_client():
    if endpoint_url := os.getenv('KINESIS_ENDPOINT_URL'):
        print(f'Local kinesis url specified: {endpoint_url}')
        return boto3.client('kinesis', endpoint_url=endpoint_url)
    else:
        return boto3.client('kinesis')


def init(prediction_stream_name: str, run_id: str, test_run: bool):
    pipeline = load_pipeline(run_id)

    callbacks = []
    if not test_run:
        kinesis_client = boto3.client('kinesis')
        kinesis_callback = KinesisCallback(
            kinesis_client, prediction_stream_name)
        callbacks.append(kinesis_callback.put_record)

    return ModelService(
        pipeline=pipeline,
        model_version=run_id,
        callbacks=callbacks,
    )
