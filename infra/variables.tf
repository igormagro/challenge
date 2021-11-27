variable "region" {
  default     = "us-east-1"
  description = "AWS region"
}

variable "tags" {
  default = {
    Author      = "Igor Magro"
    Project     = "IGTI EDC Final Challange"
    Environment = "Training"
  }
}

variable "bucket_names" {
  type = list(string)
  default = [
    "raw-zone",
    "processing-zone",
    "consumer-zone"
  ]
}

locals {
  prefix       = 370799417405
  cluster_name = "igti-edc-eks"
}

data "aws_availability_zones" "available" {}

data "aws_eks_cluster" "cluster" {
  name = module.eks.cluster_id
}

data "aws_eks_cluster_auth" "cluster" {
  name = module.eks.cluster_id
}

