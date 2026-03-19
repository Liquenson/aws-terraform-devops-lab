terraform {
  backend "s3" {
    bucket         = "devops-lab-tfstate-538079272432"
    key            = "global/s3/terraform.tfstate"
    region         = "eu-west-1"
    dynamodb_table = "devops-lab-state-lock"
    encrypt        = true
  }
}
