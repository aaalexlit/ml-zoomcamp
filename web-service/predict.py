import pickle
from flask import Flask, request, jsonify

with open('lin_reg.bin', 'rb') as f_in:
    (dv, model) = pickle.load(f_in)


def prepare_features(ride):
    return {
        'PU_DO': f"{ride['PULocationID']}_{ride['DOLocationID']}",
        'trip_distance': ride['trip_distance'],
    }


def predict(features):
    X = dv.transform(features)
    preds = model.predict(X)
    return preds[0]


app = Flask('duration-prediction')


@app.route('/predict', methods=['POST'])
def predict_endpoint():
    ride = request.get_json()
    pred = predict(prepare_features(ride))

    result = {'duration': pred}

    return jsonify(result)


if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)
