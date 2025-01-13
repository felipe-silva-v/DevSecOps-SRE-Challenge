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

## Part 2: Database Integration and Enhancements

This section describes the steps taken to extend the API to integrate with a Cloud SQL database and provide a new endpoint.

### **2.1 Database Integration**

#### **Steps Taken:**
1. Created a second Cloud SQL instance named `postgres-instance`.
   - Configured the database and ensured proper IP authorization for connectivity.
   - Used the `admin` user to create a new database `challenge_db`.
2. Connected to the database via `gcloud sql connect` and created a new table named `test_table`.
   - The table contains the following columns:
     - `id`: Primary key, auto-incrementing.
     - `column1`: VARCHAR(50).
     - `column2`: VARCHAR(255).
3. Inserted test data into the `test_table`.

#### **Table Initialization Script:**
```sql
CREATE TABLE test_table (
  id SERIAL PRIMARY KEY,
  column1 VARCHAR(50) NOT NULL,
  column2 VARCHAR(255) NOT NULL
);

INSERT INTO test_table (column1, column2) VALUES
('Test 1', 'This is the first test row'),
('Test 2', 'This is the second test row');
```

---

### **2.2 API Enhancements**

#### **Changes Made:**
1. Modified the `app.py` file to include a new `/data` endpoint.
   - The endpoint retrieves and returns all rows from `test_table` in JSON format.
2. Updated the `DATABASE` configuration in `app.py` to connect via Cloud SQL Socket:
   ```python
   "host": "/cloudsql/devsecops-sre-challenge:us-central1:postgres-instance",
   "port": 5432,
   "database": "challenge_db",
   "user": "admin",
   "password": "password123"
   ```
3. Deployed the updated application using the following commands:
   - Rebuilt and pushed the Docker image.
   - Deployed the application with Cloud SQL instance binding:
     ```bash
     gcloud run deploy flask-api \
       --image gcr.io/devsecops-sre-challenge/flask-api:latest \
       --platform managed \
       --region us-central1 \
       --allow-unauthenticated \
       --add-cloudsql-instances devsecops-sre-challenge:us-central1:postgres-instance
     ```

#### **Validation:**
Accessed the `/data` endpoint, which returned the following response:
```json
{
  "data": [
    {"id": 1, "column1": "Test 1", "column2": "This is the first test row"},
    {"id": 2, "column1": "Test 2", "column2": "This is the second test row"}
  ]
}
```

---

## Conclusion

In Part 2 of the challenge, I successfully:
1. Integrated the API with a Cloud SQL PostgreSQL database.
2. Enhanced the API to include a `/data` endpoint that interacts with the database.
3. Validated the deployment and functionality of the `/data` endpoint on Cloud Run.

The service is now capable of handling database interactions securely and efficiently.
