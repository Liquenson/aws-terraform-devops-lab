module "s3_bucket" {
  source      = "../modules/s3_bucket"
  bucket_name = var.bucket_name
  environment = var.environment
}

module "vpc" {
  source             = "../modules/vpc"
  environment        = var.environment
  vpc_cidr           = var.vpc_cidr
  public_subnets     = var.public_subnets
  private_subnets    = var.private_subnets
  availability_zones = var.availability_zones
}

module "iam" {
  source      = "../modules/iam"
  environment = var.environment
}
