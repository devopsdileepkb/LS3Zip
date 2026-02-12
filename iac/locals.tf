locals {
  project_name = "study-optimiser-aws-lambda"

  # Standardized Lambda name per environment
  lambda_name = "${local.project_name}-${var.environment}"

  # Daily schedule at 1 AM UTC
  schedule_expression = "cron(0 1 * * ? *)"
}