provider "aws" {
  region = var.region
}


terraform {
  backend "s3" {
    bucket = "370799417405-tf-backend"
    key    = "state/terraform.tfstate"
    region = "us-east-1"
  }
}