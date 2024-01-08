provider "aws" {
    region = "eu-west-3"
}

resource "aws_dynamodb_table" "my_table" {
    name = "table_1-name"
    hash_key = "Attribute_1"
    read_capacity = 1
    write_capacity = 1

    attribute {
      name = "Attribute_1"
      type = "S"
    }
}