from pathlib import Path

import model


def read_text(file):
    test_directory = Path(__file__).parent

    with open(test_directory / file, 'rt', encoding='utf-8') as f_in:
        return f_in.read().strip()


def test_base64_decode():
    base64_input = read_text('data.b64')

    actual_output = model.base64_decode(base64_input)
    expected_output = {
        "ride": {
            "PULocationID": 130,
            "DOLocationID": 205,
            "trip_distance": 3.66,
        },
        "ride_id": 156,
    }

    assert expected_output == actual_output


def test_prepare_features():
    ride = {
        "PULocationID": 130,
        "DOLocationID": 205,
        "trip_distance": 3.66,
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
    model_service = model.ModelService(
        pipeline=model_mock,
        model_version=model_version,
    )

    base64_input = read_text('data.b64')

    event = {
        "Records": [
            {
                "kinesis": {
                    "data": base64_input,
                },
            }
        ]
    }

    actual_predictions = model_service.lambda_handler(event)

    expected_predictions = [
        {
            'model': 'ride_duration_prediction_model',
            'version': model_version,
            'prediction': {'ride_duration': prediction, 'ride_id': 156},
        }
    ]

    assert expected_predictions == actual_predictions
