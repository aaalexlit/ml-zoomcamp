
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

To put an event to the kinesis queue

```bash
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