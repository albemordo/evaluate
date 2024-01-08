provider "aws" {
    region = "eu-west-3"
}

resource "aws_lb" "my_lb" {
    load_balancer_type = "application"

    subnets = [ "subnet-1234567890" ]
}