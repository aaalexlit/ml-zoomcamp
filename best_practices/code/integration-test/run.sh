#!/usr/bin/env bash

# cd to the directory where the script is
cd "$(dirname "$0")"

# give a unique tag to the docker image
LOCAL_TAG=`date +"%Y-%m-%d-%H-%M"`
export LOCAL_IMAGE_NAME="stream-model-duration:${LOCAL_TAG}"
export PREDICTIONS_STREAM_NAME="ride-predictions"

cd ..
docker compose up --build -d

sleep 5

aws --endpoint-url=http://localhost:4566 \
    kinesis create-stream \
    --stream-name ${PREDICTIONS_STREAM_NAME} \
    --shard-count 1

cd "$(dirname "$0")"
pipenv run python test_docker.py

ERROR_CODE=$?

cd ..

if [ ${ERROR_CODE} != 0 ]; then
    docker-compose logs
    docker-compose down
    exit ${ERROR_CODE}
fi

cd "$(dirname "$0")"
pipenv run python test_kinesis.py

ERROR_CODE=$?

cd ..

if [ ${ERROR_CODE} != 0 ]; then
    docker-compose logs
    docker-compose down
    exit ${ERROR_CODE}
fi

docker compose down