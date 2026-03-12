resource "aws_s3_bucket" "devops_lab_bucket" {
  bucket = var.bucket_name

  tags = {
    Name        = "DevOpsLabBucket"
    Environment = var.environment
  }
}
