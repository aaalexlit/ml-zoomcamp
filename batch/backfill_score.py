from datetime import datetime
from dateutil.relativedelta import relativedelta

import score

from prefect import flow


@flow
def ride_duration_prediction_backfill():
    start_date = datetime(year=2022, month=3, day=1)
    end_date = datetime(year=2023, month=4, day=1)

    d = start_date

    while d <= end_date:
        score.ride_duration_prediction(
            taxi_type='green',
            run_id='a4b217a84e3a44ad870271b75331eb6c',
            run_date=d
        )

        d += relativedelta(months=1)


if __name__ == '__main__':
    ride_duration_prediction_backfill()
