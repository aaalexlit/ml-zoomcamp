import json
from pathlib import Path

import requests
from deepdiff import DeepDiff

URL = "http://localhost:8080/2015-03-31/functions/function/invocations"


def test_end_to_end():
    # pylint: disable=missing-function-docstring
    with open(
        Path(__file__).parent / "kinesis_event.json", "rt", encoding="utf-8"
    ) as f_in:
        event = json.load(f_in)
    response = requests.post(url=URL, json=event, timeout=60)
    actual_response = response.json()
    print(f"actual resonse:\n{json.dumps(actual_response, indent=4)}")
    expected_response = [
        {
            "model": "ride_duration_prediction_model",
            "version": "a4b217a84e3a44ad870271b75331eb6c",
            "prediction": {"ride_duration": 18.2, "ride_id": 156},
        }
    ]
    diff = DeepDiff(actual_response, expected_response, significant_digits=1)
    print(f"diff:\n{diff}")
    # checks that diff is empty
    assert not diff


if __name__ == "__main__":
    test_end_to_end()
