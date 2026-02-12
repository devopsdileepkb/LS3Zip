variable "region" {
  description = "AWS region"
  type        = string
}

variable "environment" {
  description = "Deployment environment (dev, prd, sit, ppt)"
  type        = string
}

variable "bucket_name" {
  description = "S3 bucket name for CSV files"
  type        = string
}