# Candidate Information

Name: Felipe Silva  
Position Applied For: DevOps Engineer at LATAM Airlines  
Contact: felipe.silva@biomedica.udec.cl

---

## Part 1: Infrastructure and API Deployment

This section describes the steps I followed to complete Part 1 of the challenge, which included setting up the infrastructure, deploying a simple API, and ensuring it could be accessed publicly via Google Cloud Run.

### **1. Infrastructure Setup (Terraform)**

To manage and deploy the infrastructure, I used **Terraform**. Below are the main components of the setup:

#### **1.1 Google Cloud Resources**
I provisioned the following resources:
- **Pub/Sub Topic**: Created a topic named `data-ingestion-topic` to handle data ingestion.
- **Cloud SQL (PostgreSQL)**:
  - Created a Cloud SQL instance (`analytics-db`) using PostgreSQL version 13.
  - Configured the database with UTF8 encoding and collation (`en_US.UTF8`).
  - Created an `admin` user with a secure password for database management.
- **Cloud Run**:
  - Deployed a serverless service (`api-service`) using an image hosted on Google Container Registry (GCR).
  - Configured the service to use the default Compute Engine service account (`34181851867-compute@developer.gserviceaccount.com`).
  - Set a timeout of 3600 seconds to handle initialization delays.

#### **1.2 IAM Roles and Permissions**
To enable the service to function seamlessly:
- Assigned the role `roles/cloudsql.client` to the service account for database access.
- Assigned the role `roles/pubsub.publisher` to allow publishing messages to the Pub/Sub topic.

#### **1.3 Outputs**
Terraform was configured to output:
- **`cloud_run_url`**: The public URL of the deployed Cloud Run service.
- **`db_connection_name`**: The connection string for the Cloud SQL database.

---

### **2. API Development**

The API was developed using **Flask** to provide a simple HTTP endpoint that responds with `Hello, World!`.

#### **2.1 Application Code (`app.py`):**
The API is minimal and follows Flask best practices. It dynamically retrieves the `PORT` environment variable to ensure compatibility with Google Cloud Run and returns "Hello, World!" at the root endpoint.

#### **2.2 Dockerization**
The API was containerized using the following configuration:
- A lightweight Python image (`python:3.9-slim`) was used as the base.
- Dependencies were installed via `requirements.txt`.
- The `gunicorn` server was used to run the application in a production-ready environment.

#### **2.3 Dependency Management**
The `requirements.txt` file includes the necessary dependencies:
- Flask
- Gunicorn

---

### **3. Deployment to Cloud Run**

After building and pushing the Docker image to Google Container Registry (GCR), I used Terraform to deploy the service to **Cloud Run**.

#### **Steps:**
1. **Build and push the image:**
   - Used Docker to build and push the image to GCR.
2. **Apply Terraform changes:**
   - Terraform was used to deploy the infrastructure, including Cloud Run, Pub/Sub, and Cloud SQL.
3. **Make the service public:**
   - Used the `gcloud` command to assign public access (`roles/run.invoker`) to the service.

#### **Validation**
After deployment, I validated the service by accessing the Cloud Run URL. The service responded with `Hello, World!`, confirming that the deployment was successful.

---

## Conclusion

In Part 1 of the challenge, I successfully:
1. Set up the infrastructure using Terraform.
2. Developed and containerized a simple Flask API.
3. Deployed the API to Google Cloud Run and made it publicly accessible.
