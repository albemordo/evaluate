provider "aws" {
    region = "eu-west-3"
}

resource "aws_apigatewayv2_api" "my_apigateway" {
  name          = "example-http-api"
  protocol_type = "HTTP"
}
