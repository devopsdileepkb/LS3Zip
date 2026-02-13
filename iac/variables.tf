variable "region" {
  description = "AWS region where resources will be deployed"
  type        = string
}

variable "environment" {
  description = "Deployment environment (e.g., dev, prd, sit, ppt)"
  type        = string

  validation {
    condition     = contains(["dev", "prd", "sit", "ppt"], var.environment)
    error_message = "Environment must be one of: dev, prd, sit, ppt."
  }
}

variable "bucket_name" {
  description = "S3 bucket name for CSV files"
  type        = string

  validation {
    condition     = can(regex("^[a-z0-9.-]+$", var.bucket_name))
    error_message = "Bucket name must contain only lowercase letters, numbers, dots, and hyphens."
  }
}