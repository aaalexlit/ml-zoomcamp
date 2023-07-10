import requests

URL = 'http://localhost:8080/2015-03-31/functions/function/invocations'

event = {
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


def test_end_to_end():
    response = requests.post(url=URL, json=event)
    print(response.json())


if __name__ == '__main__':
    test_end_to_end()
