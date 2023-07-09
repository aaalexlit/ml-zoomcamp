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
