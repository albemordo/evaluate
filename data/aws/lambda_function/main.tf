provider "aws" {
    region = "eu-west-3"
}

resource "aws_lambda_function" "my_lambda" {
  filename      = "lambda_function_payload.zip"
  function_name = "lambda_function_name"
  role          = "arn:aws:lambda:eu-west-3:123456789012:function:lambda_function_name"
  handler       = "index.test"
  runtime = "nodejs18.x"
}