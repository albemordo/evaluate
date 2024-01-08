provider "aws" {
    region = "eu-west-3"
}

resource "aws_vpc" "my_vpc" {
    cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "my_subnet" {
    vpc_id = aws_vpc.my_vpc.id
    cidr_block = "10.0.1.0/24"
}

resource "aws_lb" "my_lb" {
    load_balancer_type = "application"

    subnets = [ aws_subnet.my_subnet.id ]
}