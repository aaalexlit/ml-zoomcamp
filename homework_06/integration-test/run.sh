#!/usr/bin/env bash

# cd to the directory where the script is if it's not a github action execution
if [[ -z "${GITHUB_ACTIONS}" ]]; then
  cd "$(dirname "$0")"
fi

# give a unique tag to the docker image
LOCAL_TAG=`date +"%Y-%m-%d-%H-%M"`
export LOCAL_IMAGE_NAME="batch-model-duration:${LOCAL_TAG}"

# load env vars from .env
source ../.env set

# first we start only localstack service to put the test 
# input file (fake Jan 2022 data) to S3
cd ..
docker compose up localstack -d

sleep 5

# create a bucket in localstack

aws --endpoint-url=${S3_ENDPOINT_URL} s3 mb s3://${S3_BUCKET_NAME}

# put the fake dataframe for Jan 2022 to localstack
cd "$(dirname "$0")"
pipenv run python create_test_df.py

ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    cd ..
    docker-compose logs
    docker-compose down
    exit ${ERROR_CODE}
fi

# now run the calculation
cd ..
docker compose up batch -d

sleep 5

# check that the result is as expected
cd "$(dirname "$0")"
pipenv run python integration_test.py

ERROR_CODE=$?

cd ..

if [ ${ERROR_CODE} != 0 ]; then
    docker-compose logs
    docker-compose down
    exit ${ERROR_CODE}
fi

docker compose down