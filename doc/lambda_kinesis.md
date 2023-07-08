Helpful tutorial:
https://sagarthacker.com/posts/mlops/aws-deployment-lambda-kinesis.html


The (artificial) idea is that the model is doing better predictions when the ride has already starter and that's why we want to implement it as a stream

1. Provide `AmazonKinesisAnalyticsFullAccess` to IAM user in any way (attach directly, create a group etc)
1. Create Lambda
When streams are used it's essential to provide ids to be able to idendify events cause one can't rely on the sequence of events.


Event that gets sent to the queue

```json
{
    "Records": [
        {
            "kinesis": {
                "kinesisSchemaVersion": "1.0",
                "partitionKey": "1",
                "sequenceNumber": "49641801370286448471783931287578672283018518126072430594",
                "data": "eyAgICAgICAgInJpZGUiOiB7CiAgICAgICAgICAgICJQVUxvY2F0aW9uSUQiOiAxMzAsCiAgICAgICAgICAgICJET0xvY2F0aW9uSUQiOiAyMDUsCiAgICAgICAgICAgICJ0cmlwX2Rpc3RhbmNlIjogMy42NgogICAgICAgIH0sCiAgICAgICAgInJpZGVfaWQiOiAxNTYKICAgIH0=",
                "approximateArrivalTimestamp": 1687007422.736
            },
            "eventSource": "aws:kinesis",
            "eventVersion": "1.0",
            "eventID": "shardId-000000000000:49641801370286448471783931287578672283018518126072430594",
            "eventName": "aws:kinesis:record",
            "invokeIdentityArn": "arn:aws:iam::740446032364:role/lambda-kinesis-role",
            "awsRegion": "us-west-2",
            "eventSourceARN": "arn:aws:kinesis:us-west-2:740446032364:stream/start-ride-events"
        }
    ]
}
```

To put an event to the kinesis stream using aws CLI

```bash
KINESIS_STREAM_INPUT=start-ride-events
aws kinesis put-record \
    --stream-name ${KINESIS_STREAM_INPUT} \
    --partition-key 1 \
    --data '{        "ride": {
            "PULocationID": 130,
            "DOLocationID": 205,
            "trip_distance": 3.66
        },
        "ride_id": 156
    }'  --cli-binary-format raw-in-base64-out
```

Read from stream using AWS CLI
(for that permissions need to be added)

```bash
KINESIS_STREAM_OUTPUT=ride-predictions
SHARD='shardId-000000000000'

SHARD_ITERATOR=$(aws kinesis \
    get-shard-iterator \
        --shard-id ${SHARD} \
        --shard-iterator-type TRIM_HORIZON \
        --stream-name ${KINESIS_STREAM_OUTPUT} \
        --query 'ShardIterator' \
)

RESULT=$(aws kinesis get-records --shard-iterator $SHARD_ITERATOR)

echo ${RESULT} | jq -r '.Records[0].Data' | base64 --decode | jq
```

# Dockerize lambda

1. Create pipenv to use inside the docker image
    ```shell
    pipenv install boto3 mlflow scikit-learn==1.2.2 --python=3.9
    ```

    To package lambda into a docker we need to use AWS-provided base image that contains all the required components to run your functions packaged as container images on AWS Lambda

    Python ones can be found here
    https://gallery.ecr.aws/lambda/python


1. Build docker image from the [Dockerfile](Dockerfile)
    ```shell
    docker build -t stream-model-duration:v1 .
    ```

1. Run Docker image
    ```shell
    docker run -it --rm \
    -p 8080:8080 \
    -e PREDICTIONS_STREAM_NAME="ride-predictions" \
    -e RUN_ID="a4b217a84e3a44ad870271b75331eb6c" \
    -v ~/.aws:/root/.aws \
    stream-model-duration:v1
    ```

1. Test using [test_docker.py](test_docker.py)

1. Create a repo in AWS ECR

    ```shell
    aws ecr create-repository --repository-name duration-model
    ```

1. Log into ECR with docker
    ```
    aws ecr get-login-password | docker login --username AWS --password-stdin 740446032364.dkr.ecr.us-west-2.amazonaws.com
    ```

1. Push the image
    ```
    REMOTE_URI="740446032364.dkr.ecr.us-west-2.amazonaws.com/duration-model"
    REMOTE_TAG="v1"
    REMOTE_IMAGE=${REMOTE_URI}:${REMOTE_TAG}

    LOCAL_IMAGE="stream-model-duration:v1"
    docker tag ${LOCAL_IMAGE} ${REMOTE_IMAGE}
    docker push ${REMOTE_IMAGE}
    ```

1. Create new Lambda from a container image attaching the role that permits to write to kinesis stream.

1. Set its env vars

1. Add Kinesis trigger with start-ride-event stream

1. Add s3 access permissions to the role that executes lambda

1. Increase Lambda's memory to 512 and timeout to 15 secs