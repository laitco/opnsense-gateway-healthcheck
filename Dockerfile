# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install curl for health checks
RUN apt-get update && apt-get install -y curl && apt-get clean

# Expose the port the app runs on
EXPOSE 5000

# Define default environment variables
ENV PORT=5000

# Define environment variable for Flask
ENV FLASK_APP=healthcheck.py

# Define environment variables for Gunicorn
ENV GUNICORN_TIMEOUT=120
ENV GUNICORN_GRACEFUL_TIMEOUT=120

# Define default environment variables for API configuration
ENV OPNSENSE_BASE_URL=https://opnsense.example.com
ENV OPNSENSE_PORT=443

# Add a health check to verify the container is running
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:$PORT/health || exit 1

# Set Gunicorn timeout values directly in the ENTRYPOINT
ENTRYPOINT ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "--timeout", "120", "--graceful-timeout", "120", "healthcheck:app"]