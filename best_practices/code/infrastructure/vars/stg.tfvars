consumer_kinesis_stream_name = "stg-start-ride-events"
producer_kinesis_stream_name = "stg-ride-predictions"
model_bucket_name            = "stg-mlopszoomcamp-alex"
lambda_function_local_path   = "../lambda_function.py"
docker_image_local_path      = "../Dockerfile"
ecr_repo_name                = "stg-stream-model-duration"
lambda_function_name         = "stg-prediction-lambda"