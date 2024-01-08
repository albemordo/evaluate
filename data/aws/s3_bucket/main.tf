provider "aws" {
    region = "eu-west-3"
}

resource "aws_s3_bucket" "my_bucket" {
  bucket = "my_bucket_name"
}