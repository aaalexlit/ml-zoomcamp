variable "aws_region" {
  default = "us-east-2"
}
  
variable "project_id" {
  default = "mlops-zoomcamp"
  description = "project_id"
}
  
variable "producer_kinesis_stream_name" {
  description = "Kinesis producer stream name"
}
  

variable "consumer_kinesis_stream_name" {
  description = "Kinesis consumer stream name"
}