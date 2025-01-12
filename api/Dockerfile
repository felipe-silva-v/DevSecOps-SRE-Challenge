# Use a base image for Python
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the API files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080
EXPOSE 8080

# Command to run the application
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
