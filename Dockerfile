# Use an official slim Python base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .

# Update system packages and install pip dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    supervisor \
 && rm -rf /var/lib/apt/lists/* \
 && pip install --upgrade pip \
 && pip install --default-timeout=100 --retries=10 --no-cache-dir -r requirements.txt

# Copy entire application code
COPY . .
 
# Copy supervisord configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose port
EXPOSE 8000 8501

# Start both services using supervisord
CMD ["/usr/bin/supervisord"]
