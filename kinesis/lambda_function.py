import json
import base64


def prepare_features(ride):
    features = {}
    features['PU_DO'] = f"{ride['PULocationID']}_{ride['DOLocationID']}"
    features['trip_distance'] = ride['trip_distance']
    return features


def predict(features):
    return 10.0


def lambda_handler(event, context):
    print(json.dumps(event))


    predictions = []
    for record in event['Records']:
        encoded_data = record['kinesis']['data']
        decoded_data = base64.b64decode(encoded_data).decode('utf-8')
        ride_event = json.loads(decoded_data)
        ride = ride_event['ride']
        ride_id = ride_event['ride_id']

        print(f'ride_id = {ride_id}')

        features = prepare_features(ride)
        prediction = predict(features)
        prediction_event = {
                    'model': 'ride_duration_prediction_model',
                    'version': '123',
                    'ride_duration': prediction,
                    'ride_id': ride_id
                }
        predictions.append(prediction_event)

    return predictions

