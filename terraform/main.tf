provider "aws" {
  region = "eu-west-3"
}

resource "aws_dynamodb_table" "my_table" {
  name = "my_table"
  read_capacity = 1
  write_capacity = 1
  hash_key = "Attribute_1"
  attribute {
    name = "Attribute_1"
    type = "S"
  }
}