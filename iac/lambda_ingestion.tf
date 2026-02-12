resource "aws_iam_role" "lambda_role" {
  name = "lambda_zip_csv_role_${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_policy_attach" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "zip_csv_lambda" {
  function_name = "zip-csv-lambda-${var.environment}"
  role          = aws_iam_role.lambda_role.arn
  handler       = "main.handler"
  runtime       = "python3.9"

  filename      = "${path.module}/../src/lambda/lambda.zip"

  environment {
    variables = {
      ENVIRONMENT = var.environment
      REGION      = var.region
      BUCKET      = var.bucket_name
    }
  }
}

resource "aws_s3_bucket_notification" "bucket_notify" {
  bucket = var.bucket_name

  lambda_function {
    lambda_function_arn = aws_lambda_function.zip_csv_lambda.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "iqvia_export_unload/"
    filter_suffix       = ".csv"
  }

  depends_on = [aws_lambda_function.zip_csv_lambda]
}
# EventBridge rule to trigger Lambda daily at 1 AM UTC
resource "aws_cloudwatch_event_rule" "daily_trigger" {
  name                = "zip-csv-daily-${var.environment}"
  description         = "Triggers Lambda daily at 1 AM UTC"
  schedule_expression = "cron(0 1 * * ? *)"
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.daily_trigger.name
  target_id = "zip-csv-lambda"
  arn       = aws_lambda_function.zip_csv_lambda.arn
}

# Permission for EventBridge to invoke Lambda
resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.zip_csv_lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.daily_trigger.arn
}