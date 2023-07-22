variable "stream_name" {
  type        = string
  description = "Kinesis stream name"
}

variable "shard_count" {
  type        = number
  description = "Number of shards in the stream"
}

variable "retention_period" {
  type        = number
  description = "Number of hours to retain data in the stream"
}

variable "shard_level_metrics" {
  type        = list(string)
  description = "List of shard-level metrics to enable"
  default = [
    "IncomintBytes",
    "OutgoingBytes",
    "OutgoingRecords",
    "WriteProvisionedThroughputExceeded",
    "ReadProvisionedThroughputExceeded",
    "IncomingRecords",
    "IteratorAgeMilliseconds",
  ]
}

variable "tags" {
  description = "Tags to apply to the stream"
  default     = "mlops-zoomcamp"
}
