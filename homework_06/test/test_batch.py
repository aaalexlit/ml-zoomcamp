from datetime import datetime
import pandas as pd
from deepdiff import DeepDiff
from pandas import Timestamp

import batch


def dt(hour, minute, second=0):
    return datetime(2022, 1, 1, hour, minute, second)


data = [
    (None, None, dt(1, 2), dt(1, 10)),
    (1, None, dt(1, 2), dt(1, 10)),
    (1, 2, dt(2, 2), dt(2, 3)),
    (None, 1, dt(1, 2, 0), dt(1, 2, 50)),
    (2, 3, dt(1, 2, 0), dt(1, 2, 59)),
    (3, 4, dt(1, 2, 0), dt(2, 2, 1)),
]


columns = ['PULocationID', 'DOLocationID',
           'tpep_pickup_datetime', 'tpep_dropoff_datetime']
df = pd.DataFrame(data, columns=columns)


def test_prepare_data():
    expected_dict = [{'PULocationID': '-1', 'DOLocationID': '-1', 'tpep_pickup_datetime': Timestamp('2022-01-01 01:02:00'), 'tpep_dropoff_datetime': Timestamp('2022-01-01 01:10:00'), 'duration': 8.0},
                     {'PULocationID': '1', 'DOLocationID': '-1', 'tpep_pickup_datetime': Timestamp('2022-01-01 01:02:00'),
                         'tpep_dropoff_datetime': Timestamp('2022-01-01 01:10:00'), 'duration': 8.0},
                     {'PULocationID': '1', 'DOLocationID': '2', 'tpep_pickup_datetime': Timestamp('2022-01-01 02:02:00'), 'tpep_dropoff_datetime': Timestamp('2022-01-01 02:03:00'), 'duration': 1.0},]
    categorical = ['PULocationID', 'DOLocationID']

    actual_df = batch.prepare_data(df, categorical)
    actual_dict = actual_df.to_dict(orient='records')
    diff = DeepDiff(actual_dict, expected_dict, significant_digits=1)
    print(f"diff:\n{diff}")
    assert not diff
