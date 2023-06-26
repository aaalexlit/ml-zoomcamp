import pickle

import mlflow
from flask import Flask, request, jsonify

RUN_ID = 'a4b217a84e3a44ad870271b75331eb6c'
# MLFLOW_TRACKING_URI = 'http://127.0.0.1:5000'

# mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# path = mlflow.artifacts.download_artifacts(
#     run_id=RUN_ID, artifact_path='model/model.pkl')

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
    preds = pipeline.predict(features)
    return preds[0]


app = Flask('duration-prediction')


@app.route('/predict', methods=['POST'])
def predict_endpoint():
    ride = request.get_json()
    pred = predict(prepare_features(ride))

    result = {'duration': pred}

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)
