# Use a lightweight Python image
FROM python:3.9-alpine

# Set environment variables

# Avoids writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# Ensures logs are flushed directly
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apk add --no-cache build-base libffi-dev postgresql-dev

# Copy requirements file first (leverage Docker layer caching)
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . /app

# Create a non-root user and switch to it
RUN adduser -D appuser
USER appuser

# Expose port 8080
EXPOSE 8080

# Command to run the application with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app", "--timeout", "3600"]

