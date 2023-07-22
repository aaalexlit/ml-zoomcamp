terraform {
  required_version = ">= 1.5"
  backend "s3" {
    bucket = "terraform-state-mlops-zoomcamp"
    key    = "mlops-zoomcamp.tfstate"
    region = "us-west-2"
    encrypt = true
  }
  required_providers {
    aws = "~> 5.9"
  }
}

provider "aws" {
  region = var.aws_region
  profile = "default"
}

data "aws_caller_identity" "current" {}

locals {
  account_id = data.aws_caller_identity.current.account_id
}
# start-ride-events 
module "producer_kinesis_stream" {
  source = "./modules/kinesis"
  stream_name = "${var.producer_kinesis_stream_name}-${var.project_id}"
  retention_period = 48
  shard_count = 2
  tags = var.project_id
}

# ride-predictions 
module "consumer_kinesis_stream" {
  source = "./modules/kinesis"
  stream_name = "${var.consumer_kinesis_stream_name}-${var.project_id}"
  retention_period = 48
  shard_count = 2
  tags = var.project_id
}
  
# mlopszoomcamp-alex
module "s3_bucket" {
  source = "./modules/s3"
  bucket_name = "${var.model_bucket_name}-${var.project_id}"
}