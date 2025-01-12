provider "google" {
  project = var.project_id
  region  = var.region
}

# Create Pub/Sub topic
resource "google_pubsub_topic" "data_ingestion_topic" {
  name   = "data-ingestion-topic"
  labels = {
    environment = "dev"
  }
}

# Create PostgreSQL database instance
resource "google_sql_database_instance" "analytics_db_instance" {
  name             = "analytics-db"
  database_version = "POSTGRES_13"
  region           = var.region

  settings {
    tier                  = "db-f1-micro"
    activation_policy     = "ALWAYS"
    availability_type     = "ZONAL"
    disk_autoresize       = true
    disk_type             = "PD_SSD"
    backup_configuration {
      enabled = true
    }
  }

  lifecycle {
    prevent_destroy = true
  }
}

# Create PostgreSQL database
resource "google_sql_database" "analytics_db" {
  name     = "analytics_db"
  instance = google_sql_database_instance.analytics_db_instance.name
  charset  = "UTF8"
  collation = "en_US.UTF8"

  lifecycle {
    prevent_destroy = true
  }
}

# Create a database user
resource "google_sql_user" "db_user" {
  name     = "admin"
  instance = google_sql_database_instance.analytics_db_instance.name
  password = var.db_password
}

# Deploy a serverless service on Cloud Run
resource "google_cloud_run_service" "api_service" {
  name     = "api-service"
  location = var.region

  template {
    spec {
      containers {
        image = "gcr.io/${var.project_id}/api-image:latest"
        ports {
          container_port = 8080
        }
        resources {
          limits = {
            memory = "512Mi"
            cpu    = "1"
          }
        }
      }
      timeout_seconds    = 3600
      service_account_name = "34181851867-compute@developer.gserviceaccount.com" # Default Compute Engine service account
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

# Grant permissions for the default Compute Engine service account
resource "google_project_iam_member" "cloud_run_invoker" {
  project = var.project_id
  role    = "roles/cloudsql.client"
  member  = "serviceAccount:34181851867-compute@developer.gserviceaccount.com"
}

# Add IAM policy binding for Pub/Sub
resource "google_project_iam_member" "pubsub_publisher" {
  project = var.project_id
  role    = "roles/pubsub.publisher"
  member  = "serviceAccount:34181851867-compute@developer.gserviceaccount.com"
}

# Output Cloud Run URL
output "cloud_run_url" {
  value       = google_cloud_run_service.api_service.status[0].url
  description = "The URL of the deployed Cloud Run service."
}

# Output database connection name
output "db_connection_name" {
  value       = google_sql_database_instance.analytics_db_instance.connection_name
  description = "The connection name of the Cloud SQL instance."
}
