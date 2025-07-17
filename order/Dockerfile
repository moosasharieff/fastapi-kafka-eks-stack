# Use official slim Python image for performance and security
FROM python:3.11-slim

LABEL maintainer="moosasharieff"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Pre-install only requirements file to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Default command
CMD ["uvicorn", "order.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
