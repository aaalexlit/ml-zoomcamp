terraform {
  required_version = ">= 1.5"
  backend "s3" {
    bucket  = "terraform-state-mlops-zoomcamp"
    key     = "mlops-zoomcamp.tfstate"
    region  = "us-west-2"
    encrypt = true
  }
  required_providers {
    aws = "~> 5.9"
  }
}

provider "aws" {
  region = var.aws_region
}

data "aws_caller_identity" "current" {}

locals {
  account_id = data.aws_caller_identity.current.account_id
}
# start-ride-events
module "producer_kinesis_stream" {
  source           = "./modules/kinesis"
  stream_name      = "${var.producer_kinesis_stream_name}-${var.project_id}"
  retention_period = 24
  shard_count      = 1
  tags             = var.project_id
}

# ride-predictions
module "consumer_kinesis_stream" {
  source           = "./modules/kinesis"
  stream_name      = "${var.consumer_kinesis_stream_name}-${var.project_id}"
  retention_period = 24
  shard_count      = 1
  tags             = var.project_id
}

# mlopszoomcamp-alex
module "s3_bucket" {
  source      = "./modules/s3"
  bucket_name = "${var.model_bucket_name}-${var.project_id}"
}

module "ecr_image" {
  source                     = "./modules/ecr"
  ecr_repo_name              = "${var.ecr_repo_name}-${var.project_id}"
  account_id                 = local.account_id
  lambda_function_local_path = var.lambda_function_local_path
  docker_image_local_path    = var.docker_image_local_path
}

module "lambda_function" {
  source               = "./modules/lambda"
  image_uri            = module.ecr_image.image_uri
  lambda_function_name = "${var.lambda_function_name}_${var.project_id}"
  model_bucket         = module.s3_bucket.name
  output_stream_name   = "${var.consumer_kinesis_stream_name}-${var.project_id}"
  output_stream_arn    = module.consumer_kinesis_stream.stream_arn
  source_stream_name   = "${var.producer_kinesis_stream_name}-${var.project_id}"
  source_stream_arn    = module.producer_kinesis_stream.stream_arn
}

# For CI/CD
output "lambda_function" {
  value = "${var.lambda_function_name}_${var.project_id}"
}

output "model_bucket" {
  value = module.s3_bucket.name
}

output "predictions_stream_name" {
  value = "${var.producer_kinesis_stream_name}-${var.project_id}"
}

output "ecr_repo" {
  value = "${var.ecr_repo_name}-${var.project_id}"
}
