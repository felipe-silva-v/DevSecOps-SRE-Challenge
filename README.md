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
  - Configured a Cloud SQL instance with PostgreSQL version 13 for database integration testing.
  - Set up UTF8 encoding and collation (`en_US.UTF8`).
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

### **2.1 Database Integration**

#### **Steps Taken:**
1. Set up a new Cloud SQL instance named `postgres-instance` as the production-ready database for this project.
   - Configured the database and ensured proper IP authorization for connectivity.
   - Used the `admin` user to create the `challenge_db` database, which replaced the initial setup for improved testing and final integration.
2. Connected to the database via `gcloud sql connect` and created a new table named `test_table` for data handling during testing.
   - The table contains the following columns:
     - `id`: Primary key, auto-incrementing.
     - `column1`: VARCHAR(50).
     - `column2`: VARCHAR(255).
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

### **CI/CD Integration**

The CI/CD pipeline implemented for this project automates the process of building, publishing, and deploying the Flask API. Below are the main steps:

1. **Code Build**:
   - Each update triggers the build process where a new Docker image is created for the API:
     ```bash
     docker build -t flask-api .
     ```

2. **Image Tagging and Push**:
   - The Docker image is tagged and pushed to Google Container Registry (GCR):
     ```bash
     docker tag flask-api gcr.io/devsecops-sre-challenge/flask-api:latest
     docker push gcr.io/devsecops-sre-challenge/flask-api:latest
     ```

3. **Automated Deployment**:
   - The pipeline uses `gcloud run deploy` to update the Cloud Run service with the latest image:
     ```bash
     gcloud run deploy flask-api \
       --image gcr.io/devsecops-sre-challenge/flask-api:latest \
       --platform managed \
       --region us-central1 \
       --allow-unauthenticated \
       --add-cloudsql-instances devsecops-sre-challenge:us-central1:postgres-instance
     ```

This CI/CD process ensures that all changes made to the application are automatically deployed to the cloud, keeping the service up-to-date without manual intervention. Logs and execution details of the pipeline are visible in the Git repository for auditing and monitoring purposes.

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

In this part of the challenge, I successfully:
1. Integrated the API with a Cloud SQL PostgreSQL database.
2. Enhanced the API to include a `/data` endpoint that interacts with the database.
3. Validated the deployment and functionality of the `/data` endpoint on Cloud Run.

The service is now capable of handling database interactions securely and efficiently.

### 2.3 Pub/Sub Listener and Database Integration

#### **Objective**
Implement a Pub/Sub listener to process messages and save the data to a PostgreSQL database hosted on Google Cloud SQL.

#### **Implementation**
1. **Google Cloud Pub/Sub**
   - A Pub/Sub topic (`ingestion-topic`) was created to publish messages.
   - A subscription (`ingestion-topic-sub`) was created to listen to the topic.

2. **Listener Script**
   - A Python script (`pubsub_listener.py`) was implemented to:
     - Listen for messages from the `ingestion-topic-sub` subscription.
     - Validate the received data.
     - Save the data into a PostgreSQL database table (`users`).

3. **Database Integration**
   - The previous database was deleted, and a new table `users` was created with the following structure:
     ```sql
     CREATE TABLE users (
         user_id SERIAL PRIMARY KEY,
         email VARCHAR(255) NOT NULL,
         name VARCHAR(255) NOT NULL
     );
     ```
   - The table was pre-populated with 6 records for testing purposes:
     ```sql
     INSERT INTO users (email, name) VALUES
     ('john.doe@example.com', 'John Doe'),
     ('jane.smith@example.com', 'Jane Smith'),
     ('alice.johnson@example.com', 'Alice Johnson'),
     ('bob.miller@example.com', 'Bob Miller'),
     ('charlie.brown@example.com', 'Charlie Brown'),
     ('diana.prince@example.com', 'Diana Prince');
     ```

4. **Cloud SQL Proxy**
   - The Cloud SQL Proxy is used to establish a secure connection between the local machine and the Cloud SQL instance.
   - The proxy listens on the `/cloudsql` socket or optionally on a local TCP port.

5. **Testing**
   - Messages are published to the Pub/Sub topic using:
     ```bash
     gcloud pubsub topics publish ingestion-topic --message '{"user_id": 7, "email": "linda.williams@example.com", "name": "Linda Williams"}'
     ```
   - The script processes the message and inserts it into the `users` table.
   - Data is verified in the database with:
     ```sql
     SELECT * FROM users;
     ```

#### **Automating the Deployment**

To avoid manually running the Pub/Sub listener script and the Cloud SQL Proxy, the system can be deployed using **Cloud Run** for automation and scalability.

##### **Deploying to Cloud Run**
1. **Containerization**
   - The Pub/Sub listener script can be containerized using a `Dockerfile` for environment compatibility. Detailed instructions are available in the project.

2. **Deployment**
   - The container can be built and deployed to Cloud Run using:
     ```bash
     gcloud run deploy pubsub-listener \
         --image gcr.io/PROJECT_ID/pubsub-listener \
         --add-cloudsql-instances PROJECT_ID:REGION:INSTANCE_NAME \
         --platform managed \
         --region REGION \
         --allow-unauthenticated
     ```

##### **Push Subscriptions**
Alternatively, configure a **Push Subscription** to send Pub/Sub messages directly to an API endpoint.

1. Update your API to handle Pub/Sub messages:
   - The API receives messages and processes them into the database.

2. Create a push subscription:
   ```bash
   gcloud pubsub subscriptions create ingestion-topic-push \
       --topic=ingestion-topic \
       --push-endpoint=https://YOUR_API_ENDPOINT/pubsub \
       --push-auth-service-account=SERVICE_ACCOUNT_EMAIL
   ```

#### **Benefits of Automation**
- Eliminates the need to manually run the listener and Cloud SQL Proxy.
- Provides a scalable and managed solution using Cloud Run or Push Subscriptions.
- Simplifies integration with CI/CD pipelines and production environments.

---

This concludes the implementation of **2.3** with recommendations for automation and deployment to production environments.

---

### **2.4 Architecture Diagram**

The architecture diagram below represents the infrastructure outlined in Section 1.1. It showcases the end-to-end process of how data flows through the system, covering ingestion, storage, and exposure via an HTTP API.

#### **Diagram Overview**
The diagram demonstrates three key stages in the system architecture:
1. **Data Ingestion:**
   - **Clients or Applications** publish data in JSON format to the **Pub/Sub Topic**. This ensures asynchronous and scalable ingestion of data.
   - The **Pub/Sub Subscription** delivers these messages to the system, enabling downstream components to process and store the data.

2. **Data Storage:**
   - Messages delivered by the subscription are stored in the **Cloud SQL Database** (PostgreSQL).

3. **Data Exposure:**
   - The **API**, hosted on **Cloud Run**, interacts with the database to query and retrieve stored data.
   - Consumers, such as browsers or applications, send HTTP GET requests to the API’s exposed endpoint (e.g., ```/data```), which responds with the requested data in JSON format.

#### **Component Roles**

- **Pub/Sub Topic and Subscription:** Serve as the ingestion layer, ensuring reliable and asynchronous delivery of messages.
- **Cloud SQL Database:** Provides structured storage for ingested data, making it easily accessible for downstream applications.
- **API (Cloud Run):** Acts as the interface between the database and external consumers, exposing data through HTTP endpoints.
- **Client/Application and Consumer:** Represent the external entities interacting with the system by publishing data and consuming it via the API.

#### **Diagram Reference**
![Architecture Diagram](diagrams/architecture.png)

This diagram encapsulates the flow of data across the system, highlighting the interactions between the components. It provides a clear view of how data is ingested, stored, and made accessible to external consumers through an API.

---
