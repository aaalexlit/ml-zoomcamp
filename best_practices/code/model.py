import json
import os
import pickle
import base64

import boto3
import mlflow


# kinesis_client = boto3.client('kinesis')

def load_pipeline(run_id: str):
    path = mlflow.artifacts.download_artifacts(
        artifact_uri=f"s3://mlopszoomcamp-alex/1/{run_id}/artifacts/model/model.pkl")
    with open(path, 'rb') as f_out:
        return pickle.load(f_out)


class ModelService:

    def __init__(self, pipeline, prediction_stream_name, test_run):
        self.pipeline = pipeline
        self.prediction_stream_name = prediction_stream_name
        self.test_run = test_run

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
            decoded_data = base64.b64decode(encoded_data).decode('utf-8')
            ride_event = json.loads(decoded_data)
            ride = ride_event['ride']
            ride_id = ride_event['ride_id']

            features = self.prepare_features(ride)
            prediction = self.predict(features)
            prediction_event = {
                'model': 'ride_duration_prediction_model',
                'version': '123',
                'prediction': {
                    'ride_duration': prediction,
                    'ride_id': ride_id
                }
            }
            if not self.test_run:
                kinesis_client.put_record(
                    StreamName=self.prediction_stream_name,
                    Data=json.dumps(prediction_event),
                    PartitionKey='1',
                )
            predictions.append(prediction_event)
        return predictions


def init(prediction_stream_name: str, run_id: str, test_run: bool):
    pipeline = load_pipeline(run_id)
    return ModelService(
        pipeline=pipeline, 
        prediction_stream_name=prediction_stream_name, 
        test_run=test_run
    )
