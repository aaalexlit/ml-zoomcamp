from datetime import timedelta
from pathlib import Path
import requests
from prefect import flow, task
from prefect.tasks import task_input_hash
from prefect_aws import S3Bucket


@task(retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=30))
def download_locally(base_url: str, file_name: str) -> Path:
    """Download files locally to then upload them to S3"""
    filepath = Path(f"data/{file_name}")
    if not filepath.exists():
        url = base_url + file_name
        response = requests.get(url, timeout=100)
        with open(filepath, 'wb') as f:
            f.write(response.content)
    return filepath


@task
def upload_to_s3(path: Path) -> None:
    """Upload local parquet file to s3"""
    s3_bucket_block = S3Bucket.load('taxi-s3-bucket')
    s3_bucket_block.upload_from_path(from_path=path, to_path=path)

@flow()
def web_to_s3(months: list[int] = [1, 2], year: int = 2021, color: str = "yellow"):
    for month in months:
        file_name = f"{color}_tripdata_{year}-{month:02}.parquet"
        base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/"
        path = download_locally(base_url=base_url, file_name=file_name)
        upload_to_s3(path)


if __name__ == "__main__":
    color = "green"
    months = [1, 2]
    year = 2021
    web_to_s3(months, year, color)
