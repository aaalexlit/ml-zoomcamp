import pickle
import pandas as pd


get_ipython().system('wget -nc https://github.com/DataTalksClub/mlops-zoomcamp/raw/main/cohorts/2023/04-deployment/homework/model.bin')


with open('model.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)


categorical = ['PULocationID', 'DOLocationID']

def read_data(filename):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df


year = 2022
month = 2
taxi_type = 'yellow'
df = read_data(f'https://d37ci6vzurychx.cloudfront.net/trip-data/{taxi_type}_tripdata_{year:04d}-{month:02d}.parquet')
df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')



dicts = df[categorical].to_dict(orient='records')
X_val = dv.transform(dicts)
y_pred = model.predict(X_val)



round(y_pred.std(), 2)


df_result = pd.DataFrame()
df_result['ride_id'] = df['ride_id']
df_result['predicted_duration'] = y_pred




output_file = f'../data/predicted_duration_{taxi_type}_tripdata_{year:04d}-{month:02d}.parquet'



df_result.to_parquet(
    output_file,
    engine='pyarrow',
    compression=None,
    index=False
)



get_ipython().system('ls -lh ../data/{output_file}')






