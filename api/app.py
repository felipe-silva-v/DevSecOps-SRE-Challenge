import os
from flask import Flask

# Create a Flask application instance
app = Flask(__name__)

# Define the root route
@app.route("/")
def hello_world():
    return "Hello, World!"  # Return a simple response

if __name__ == "__main__":
    # Get the port from the PORT environment variable, default to 8080
    port = int(os.environ.get("PORT", 8080))
    # Start the Flask application and listen on all interfaces (0.0.0.0)
    app.run(host="0.0.0.0", port=port)
