import os
import sys

import pandas as pd
from pandas import Timestamp

# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))

# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)

# adding the parent directory to
# the sys.path.
sys.path.append(parent)

from batch import get_output_path, get_storage_options


def integration_test():
    expected_prediction = pd.read_parquet('expected_prediction.parquet')
    output_file_path = get_output_path(2022, 1)
    actual_prediction = pd.read_parquet(
        output_file_path, storage_options=get_storage_options(output_file_path))
    assert actual_prediction.equals(expected_prediction)
    print('predicted dataframe is the same as expected dataframe')


if __name__ == "__main__":
    integration_test()
