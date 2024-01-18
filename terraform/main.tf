provider "aws" {
  region = "us-west-2"
}

resource "aws_iam_role" "lambda_role" {
  name = "lambda_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        },
      },
    ],
  })
}

resource "aws_lambda_function" "example" {
  function_name = "lambda_function_name"

  s3_bucket     = "my_lambda_functions"
  s3_key        = "function.zip"

  handler       = "index.handler"
  runtime       = "nodejs12.x"

  role          = aws_iam_role.lambda_role.arn
}
