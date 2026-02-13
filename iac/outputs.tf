output "lambda_function_name" {
  description = "Name of the Lambda function"
  value       = aws_lambda_function.zip_csv_lambda.function_name
}

output "lambda_function_arn" {
  description = "ARN of the Lambda function"
  value       = aws_lambda_function.zip_csv_lambda.arn
}

output "lambda_role_name" {
  description = "Name of the IAM role for Lambda"
  value       = aws_iam_role.lambda_role.name
}

output "lambda_role_arn" {
  description = "ARN of the IAM role for Lambda"
  value       = aws_iam_role.lambda_role.arn
}

output "s3_bucket_name" {
  description = "Name of the S3 bucket used by Lambda"
  value       = var.bucket_name
}

output "eventbridge_rule_name" {
  description = "Name of the EventBridge rule that triggers Lambda daily"
  value       = aws_cloudwatch_event_rule.daily_trigger.name
}

output "eventbridge_rule_arn" {
  description = "ARN of the EventBridge rule that triggers Lambda daily"
  value       = aws_cloudwatch_event_rule.daily_trigger.arn
}