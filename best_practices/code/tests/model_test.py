import model


def test_base64_decode():
    base64_input = 'eyAgICAgICAgInJpZGUiOiB7CiAgICAgICAgICAgICJQVUxvY2F0aW9uSUQiOiAxMzAsCiAgICAgICAgICAgICJET0xvY2F0aW9uSUQiOiAyMDUsCiAgICAgICAgICAgICJ0cmlwX2Rpc3RhbmNlIjogMy42NgogICAgICAgIH0sCiAgICAgICAgInJpZGVfaWQiOiAxNTYKICAgIH0='

    actual_output = model.base64_decode(base64_input)
    expected_output = {"ride": {
        "PULocationID": 130,
        "DOLocationID": 205,
        "trip_distance": 3.66
    },
        "ride_id": 156
    }

    assert expected_output == actual_output


def test_prepare_features():
    ride = {
        "PULocationID": 130,
        "DOLocationID": 205,
        "trip_distance": 3.66
    }

    model_service = model.ModelService(None, None, True)

    actual_features = model_service.prepare_features(ride)

    expected_features = {
        'PU_DO': '130_205',
        'trip_distance': 3.66,
    }

    assert actual_features == expected_features


def test_predict():
    expected_prediction = 10.0
    model_mock = ModelMock(expected_prediction)
    model_service = model.ModelService(model_mock)

    features = {
        'PU_DO': '130_205',
        'trip_distance': 3.66,
    }

    actual_prediction = model_service.predict(features)

    assert actual_prediction == expected_prediction


class ModelMock:
    def __init__(self, value):
        self.value = value

    def predict(self, X):
        n = len(X)
        return [self.value] * n


def test_lambda_handler():
    prediction = 10.0
    model_mock = ModelMock(prediction)
    model_version = 'test123'
    model_service = model.ModelService(pipeline=model_mock,
                                       model_version=model_version,
                                       )

    event = {
        "Records": [
            {
                "kinesis": {
                    "data": "eyAgICAgICAgInJpZGUiOiB7CiAgICAgICAgICAgICJQVUxvY2F0aW9uSUQiOiAxMzAsCiAgICAgICAgICAgICJET0xvY2F0aW9uSUQiOiAyMDUsCiAgICAgICAgICAgICJ0cmlwX2Rpc3RhbmNlIjogMy42NgogICAgICAgIH0sCiAgICAgICAgInJpZGVfaWQiOiAxNTYKICAgIH0=",
                },
            }
        ]
    }

    actual_predictions = model_service.lambda_handler(event)

    expected_predictions = [{
        'model': 'ride_duration_prediction_model',
        'version': model_version,
        'prediction': {
            'ride_duration': prediction,
            'ride_id': 156
        }
    }]

    assert expected_predictions == actual_predictions
