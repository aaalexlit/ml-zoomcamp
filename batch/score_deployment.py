from score import ride_duration_prediction

from prefect.deployments import Deployment
from prefect.server.schemas.schedules import CronSchedule

deployment = Deployment.build_from_flow(
    flow=ride_duration_prediction,
    name="ride_duration_prediction",
    parameters={
        "taxi_type": "green",
        "run_id": "a4b217a84e3a44ad870271b75331eb6c",
    },
    schedule=CronSchedule(cron="0 3 2 * *"),
    work_pool_name="mlops-zoomcamp-pool"
)

deployment.apply()
