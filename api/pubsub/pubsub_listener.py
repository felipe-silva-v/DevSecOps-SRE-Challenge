import os
import json
import logging
import psycopg2
from google.cloud import pubsub_v1

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure your project and subscription
project_id = "devsecops-sre-challenge"
subscription_id = "ingestion-topic-sub"

def validate_data(data):
    """Validate incoming data."""
    required_keys = ["user_id", "email", "name"]  # Example of keys
    for key in required_keys:
        if key not in data:
            raise ValueError(f"Missing required key: {key}")

def save_to_database(data):
    """Save data to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            host="/cloudsql/devsecops-sre-challenge:us-central1:postgres-instance",
            port=5432,
            database="challenge_db",
            user="admin",
            password="password123"
        )
        cursor = conn.cursor()
        # Insert data into the `users` table
        cursor.execute(
            "INSERT INTO users (user_id, email, name) VALUES (%s, %s, %s)",
            (data["user_id"], data["email"], data["name"])
        )
        conn.commit()
        cursor.close()
        conn.close()
        logger.info("Data saved successfully to the database.")
    except Exception as e:
        logger.error(f"Error saving data to the database: {e}")

def callback(message):
    """Process incoming messages from Pub/Sub."""
    logger.info(f"Message received: {message.data}")
    try:
        # Parse and validate the message
        data = json.loads(message.data.decode("utf-8"))
        validate_data(data)
        save_to_database(data)  # Save data to the database
        logger.info(f"Processed data: {data}")
        message.ack()  # Confirm message processing
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        message.nack()
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        message.ack()
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        message.nack()

def main():
    """Main function to receive messages."""
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        raise EnvironmentError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
    
    try:
        subscriber = pubsub_v1.SubscriberClient()
        subscription_path = subscriber.subscription_path(project_id, subscription_id)

        logger.info(f"Listening for messages on: {subscription_path}")
        streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

        streaming_pull_future.result()  # Block and listen for messages
    except KeyboardInterrupt:
        streaming_pull_future.cancel()
        logger.info("Streaming pull interrupted.")
    finally:
        subscriber.close()

if __name__ == "__main__":
    main()
