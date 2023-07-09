import json
import os
import pickle
import base64

import boto3
import mlflow

PREDICTIONS_STREAM_NAME = os.getenv(
    'PREDICTIONS_STREAM_NAME', 'ride-predictions')
kinesis_client = boto3.client('kinesis')

RUN_ID = os.getenv('RUN_ID', 'a4b217a84e3a44ad870271b75331eb6c')

path = mlflow.artifacts.download_artifacts(
    artifact_uri=f"s3://mlopszoomcamp-alex/1/{RUN_ID}/artifacts/model/model.pkl")

with open(path, 'rb') as f_out:
    pipeline = pickle.load(f_out)

def prepare_features(ride):
    return {
        'PU_DO': f"{ride['PULocationID']}_{ride['DOLocationID']}",
        'trip_distance': ride['trip_distance'],
    }


def predict(features):
    return pipeline.predict(features)[0]


def lambda_handler(event, context):
    # print(json.dumps(event))

    predictions = []
    for record in event['Records']:
        encoded_data = record['kinesis']['data']
        decoded_data = base64.b64decode(encoded_data).decode('utf-8')
        ride_event = json.loads(decoded_data)
        ride = ride_event['ride']
        ride_id = ride_event['ride_id']

        # print(f'ride_id = {ride_id}')

        features = prepare_features(ride)
        prediction = predict(features)
        prediction_event = {
            'model': 'ride_duration_prediction_model',
            'version': '123',
            'prediction': {
                'ride_duration': prediction,
                'ride_id': ride_id
            }
        }

        kinesis_client.put_record(
            StreamName=PREDICTIONS_STREAM_NAME,
            Data=json.dumps(prediction_event),
            PartitionKey='1',
        )
        predictions.append(prediction_event)

    return predictions
