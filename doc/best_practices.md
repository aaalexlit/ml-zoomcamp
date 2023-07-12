1. Copy files from streaming lecture to a new folder
    From the project root

    ```shell
    cp -r kinesis/ best_practices/code 
    ```
1. Create a pipenv virtual environment

    ```shell
    pipenv install
    ```

1. Add dev dependency `pytest`
    ```shell
    pipenv install --dev pytest
    ```

1. check that it's properly installec
    ```shell
    pipenv run which pytest
    ```
1. Configure Testing tab in Visual Studio Code and select pytest

1. The following env vars need to be exported

    ```bash
    export RUN_ID=a4b217a84e3a44ad870271b75331eb6c
    export TEST_RUN=True
    ```

1. Build docker image from [Dockerfile](../best_practices/code/Dockerfile)
    ```bash
    docker build -t stream-model-duration:v2 .
    ```

1. Run the built docker image
    ```bash
    docker run -it --rm \
    -p 8080:8080 \
    -e PREDICTIONS_STREAM_NAME="ride-predictions" \
    -e RUN_ID="a4b217a84e3a44ad870271b75331eb6c" \
    -e TEST_RUN="True" \
    -v ~/.aws:/root/.aws \
    stream-model-duration:v2    
    ```

1. Run tests from CLI

    ```shell
    pipenv run pytest tests/
    ```

1. install deepdiff (development) dependency

    ```shell
    pipenv install --dev deepdiff
    ```

1. run integration test from CLI (docker image needs to be running) [test_docker.py](../best_practices/code/integraton-test/test_docker.py)

    ```shell
    python test_docker.py
    ```

## Run integration tests against the model downloaded from the s3 locally

1. Copy files from s3 to [integraton-test/model/](../best_practices/code/integraton-test/model/) folder
    ```shell
    aws s3 cp --recursive s3://mlopszoomcamp-alex/1/a4b217a84e3a44ad870271b75331eb6c/artifacts/model .
    ```

1. Specify model path for in docker run and mount it as a volume

    ```shell
    docker run -it --rm \
    -p 8080:8080 \
    -e PREDICTIONS_STREAM_NAME="ride-predictions" \
    -e RUN_ID="a4b217a84e3a44ad870271b75331eb6c" \
    -e TEST_RUN="True" \
    -e MODEL_LOCATION="/app/model/model.pkl" \
    -v $(pwd)/integration-test/model:/app/model \
    -v ~/.aws:/root/.aws \
    stream-model-duration:v2 
    ```

## Automate the test using a shell script

Create [run.sh](../best_practices/run.sh)

Make it executable

```shell
chmod +x run.sh
```

Execute the sript from any directory eg from [best_practices/code/](../best_practices/code/)
```shell
./integration-test/run.sh
```

## Test kinesis with localstack using an image

To test spinning up only kinesis part of docker-compose:
```shell
docker compose up kinesis
```

To list streams in kinesis in the AWS account
```shell
aws kinesis list-streams
```

To go to lockalstack instead

```shell
aws --endpoint-url=http://localhost:4566 kinesis list-streams 
```

Create kinesis stream `ride-predictions` on localstack

```shell
aws --endpoint-url=http://localhost:4566 \
    kinesis create-stream \
    --stream-name ride-predictions \
    --shard-count 1
```

Now we need to configure the code to connect to http://localhost:4566 instead of trying to connect to AWS

Add env var `- KINESIS_ENDPOINT_URL=http://kinesis:4566/`

then run [run.sh](../best_practices/code/integration-test/run.sh)

first comment the `docker compose down` part to be able to check the kinesis stream

when it's done run the following

```bash
KINESIS_STREAM_OUTPUT=ride-predictions
SHARD='shardId-000000000000'

aws --endpoint-url=http://localhost:4566 \
        kinesis get-shard-iterator \
        --shard-id ${SHARD} \
        --shard-iterator-type TRIM_HORIZON \
        --stream-name ${KINESIS_STREAM_OUTPUT} \
        --query 'ShardIterator' \

aws --endpoint-url=http://localhost:4566 kinesis get-records --shard-iterator "AAAAAAAAAAFBGMKbwnfd9XFDEFzCKFZ+BZNTmSUr+V7VA6LNRueML8apWHxaNUzYJO1HiZDzD5TfNHTS15tu+SIPeH054ph8MJB3nwPeFf6z6rkySbH50U0a8T508siTDQhYvM+jBjnmcILxJRlD0QanT26Ezk9VBuX5CyjO97CkXlxepSV+fFvV3a9hhVsZrdMdy0EP0OfOy9gxiwoP+3Ek7ZeK52zN"

echo "eyJtb2RlbCI6ICJya
WRlX2R1cmF0aW9uX3ByZWRpY3Rpb25fbW9kZWwiLCAidmVyc2lvbiI6ICJhNGIyMTdhODRlM2E0NGFkODcwMjcxYjc1MzMxZWI2Yy
IsICJwcmVkaWN0aW9uIjogeyJyaWRlX2R1cmF0aW9uIjogMTguMTY4OTQ1NzI2NDA1MzI2LCAicmlkZV9pZCI6IDE1Nn19" | base64 -d
```

