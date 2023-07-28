variable "aws_region" {
  default = "us-west-2"
}
  
variable "project_id" {
  default = "mlops-zoomcamp"
  description = "project_id"
}
  
variable "producer_kinesis_stream_name" {
  description = "Kinesis stream name for predictions"
}
  

variable "consumer_kinesis_stream_name" {
  description = "Kinesis stream name for start ride events"
}

variable "model_bucket_name" {
  description = "Name of the S3 bucket to store models"
}

variable "ecr_repo_name" {
  description = "Name of the ECR repository"
}
  
variable "lambda_function_local_path" {
  description = "Path to the lambda function"
}

variable "docker_image_local_path" {
  description = "Path to the docker image"
}
  
variable "lambda_function_name" {
  description = "value of the lambda function name"
}