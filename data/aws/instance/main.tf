provider "aws" {
    region = "eu-west-3"
}

resource "aws_instance" "my_instance" {
  ami = "ami-1234567890"
  instance_type = "t2.micro"
  vpc_security_group_ids = [ "sg-abcde12345" ]
}