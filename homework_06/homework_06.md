1. Create pipenv virtual environment 
```shell
pipenv install
```

1. Check that everything still works after refactor

```shell
pipenv run python batch.py 2022 2
```

1. install pytest

```shell
pipenv install --dev pytest
```

Spin up just localstack service in docker compose

```shell
docker compose up localstack -d
```

create an s3 bucket there
```shell
aws --endpoint-url=http://localhost:4566/ s3 mb s3://nyc-duration
```

check that the bucket has been created
```shell
aws --endpoint-url=http://localhost:4566/ s3 ls
```

---
### Test the version that reads from s3 bucket

1. Download the file

    ```shell
    curl --output yellow_tripdata_2022-02.parquet https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-02.parquet
    ```

1. Copy it into the running localstack

    ```shell
    aws --endpoint-url=http://localhost:4566/ s3 cp yellow_tripdata_2022-02.parquet s3://nyc-duration/in/2022-02.parquet
    ```

---

## Important! 

All the environment variables need to be set through the [.env](.env) file

### Example:

```shell
export S3_ENDPOINT_URL="http://localhost:4566/"
export S3_BUCKET_NAME="nyc-duration"
export INPUT_FILE_PATTERN="s3://${S3_BUCKET_NAME}/in/{year:04d}-{month:02d}.parquet"
export OUTPUT_FILE_PATTERN="s3://${S3_BUCKET_NAME}/out/{year:04d}-{month:02d}.parquet"
```

---