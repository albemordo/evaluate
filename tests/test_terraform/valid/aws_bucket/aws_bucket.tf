provider "aws" {
    region = "eu-west-3"
}

resource "aws_s3_bucket" "random_bucket" {
    bucket = "mordo_lol"
}