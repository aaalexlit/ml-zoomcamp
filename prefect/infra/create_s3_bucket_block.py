from time import sleep
from prefect_aws import S3Bucket, AwsCredentials
from dotenv import load_dotenv
import os

load_dotenv()

def create_aws_creds_block():
    """Create a block for AWS creds"""
    AwsCredentials(
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
    ).save(name='aws-creds', overwrite=True)


def create_s3_bucket_block():
    """Create a block for AWS S3 bucket"""
    aws_creds = AwsCredentials.load('aws-creds')
    s3_bucket_object = S3Bucket(
        bucket_name='mlopszoomcamp-alex',
        credentials=aws_creds
    )
    s3_bucket_object.save(
        name='taxi-s3-bucket',
        overwrite=True
    )


if __name__=='__main__':
    create_aws_creds_block()
    sleep(10)
    create_s3_bucket_block()
