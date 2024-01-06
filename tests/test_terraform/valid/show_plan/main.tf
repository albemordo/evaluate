provider "aws" {
    region = "eu-west-3"
}

resource "aws_instance" "my_instance" {
    ami = data.aws_ami.my_ami.id
    instance_type = "t2.micro"
}

data "aws_ami" "my_ami" {
    most_recent = true
    owners      = ["amazon"]
    filter {
        name   = "architecture"
        values = ["arm64"]
    }
    filter {
        name   = "name"
        values = ["al2023-ami-2023*"]
    }
}
