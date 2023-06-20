import pickle
import sys
from pathlib import Path
import pandas as pd
import numpy as np

categorical = ["PULocationID", "DOLocationID"]

def load_model():
    with open("model.bin", "rb") as f_in:
        dv, model = pickle.load(f_in)
    return dv, model


def read_data(filename, year, month):
    df = pd.read_parquet(filename)

    df["ride_id"] = f"{year:04d}/{month:02d}_" + df.index.astype("str")

    df["duration"] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df["duration"] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype("int").astype("str")

    return df


def save_results(df, y_pred, output_file):
    df_result = pd.DataFrame()
    df_result["ride_id"] = df["ride_id"]
    df_result["predicted_duration"] = y_pred

    Path(output_file).parent.mkdir(parents=True, exist_ok=True)

    df_result.to_parquet(output_file, engine="pyarrow",
                         compression=None, index=False)


def prepare_features(df, dv):
    dicts = df[categorical].to_dict(orient="records")
    return dv.transform(dicts)


def apply_model(input_file: str, output_file: str, year: int, month: int) -> None:
    print(f'reading the data from the {input_file}...')
    df = read_data(input_file, year, month)

    print('loading the model...')
    dv, model = load_model()
    print('applying the model...')
    features = prepare_features(df, dv)
    y_pred = model.predict(features)

    print(np.mean(y_pred))

    print(f'saving the results to {output_file}...')
    save_results(df, y_pred, output_file)
    return output_file


def get_paths(year, month, taxi_type) -> tuple[str, str]:
    input_file = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{taxi_type}_tripdata_{year:04d}-{month:02d}.parquet"
    output_file = f"../data/predicted_duration_{taxi_type}_tripdata_{year:04d}-{month:02d}.parquet"
    return input_file, output_file


def ride_duration_prediction(taxi_type: str, year: int, month: int):
    input_file, output_file = get_paths(year=year,
                                        month=month,
                                        taxi_type=taxi_type)

    apply_model(input_file, output_file, year, month)


def run():
    taxi_type = sys.argv[1]  # 'yellow'
    year = int(sys.argv[2])  # 2022
    month = int(sys.argv[3])  # 3
    ride_duration_prediction(taxi_type, year, month)


if __name__ == "__main__":
    run()
