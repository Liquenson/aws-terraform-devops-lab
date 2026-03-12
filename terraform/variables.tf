variable "bucket_name" {
  description = "Nombre del bucket"
  type        = string
}

variable "environment" {
  description = "Entorno"
  type        = string
  default     = "dev"
}