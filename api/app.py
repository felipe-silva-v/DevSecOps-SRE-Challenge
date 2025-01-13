import os
import psycopg2
from flask import Flask, jsonify

# Database connection configuration
DATABASE = {
    "host": "/cloudsql/devsecops-sre-challenge:us-central1:postgres-instance",  # socket connection
    "port": 5432,
    "database": "challenge_db",  # Database name for the challenge
    "user": "admin",            # Username for the database
    "password": "password123"      # Password for the database
}

def get_db_connection():
    """Create a new database connection."""
    try:
        conn = psycopg2.connect(
            host=DATABASE["host"],
            port=DATABASE["port"],
            database=DATABASE["database"],
            user=DATABASE["user"],
            password=DATABASE["password"]
        )
        return conn
    except Exception as e:
        raise RuntimeError(f"Database connection failed: {str(e)}")

# Create a Flask application instance
app = Flask(__name__)

# Root route for health check
@app.route("/")
def health_check():
    """Health check endpoint to confirm the API is running."""
    return jsonify({"message": "API is running successfully!"}), 200

# Route to fetch data from the database
@app.route("/data", methods=["GET"])
def get_data():
    """Fetch data from the database and return it as JSON."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Execute query to fetch data from the specified table
        cursor.execute("SELECT * FROM test_table;")  # Query the test_table instead of your_table_name
        rows = cursor.fetchall()
        # Convert data to JSON format
        data = [
            {"id": row[0], "column1": row[1], "column2": row[2]} for row in rows
        ]
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Ensure the connection and cursor are properly closed
        cursor.close()
        conn.close()

    return jsonify({"data": data})

if __name__ == "__main__":
    # Get the port from the PORT environment variable, default to 8080
    port = int(os.environ.get("PORT", 8080))
    # Start the Flask application and listen on all interfaces (0.0.0.0)
    app.run(host="0.0.0.0", port=port)
