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
                "data": "Hellothisisatest",
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

