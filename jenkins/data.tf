

data "aws_availability_zones" "azs" {}

provider "aws" {
  region = "ap-south-1"
}