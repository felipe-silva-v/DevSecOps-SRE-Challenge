# Variable for the GCP Project ID
variable "project_id" {
  description = "The ID of the GCP project where the resources will be deployed"
  default     = "devsecops-sre-challenge" # Project ID
}

# Variable for the region
variable "region" {
  description = "The region where the resources will be deployed"
  default     = "us-central1" # region
}

# Variable for the database password
variable "db_password" {
  description = "Password for the PostgreSQL database user"
  default     = "mypassword.123"
  sensitive   = true
}
