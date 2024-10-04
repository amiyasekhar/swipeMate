FROM python:3.11-slim

# Install system packages needed for gpgme and other dependencies
RUN apt-get update && apt-get install -y \
    libgpgme-dev \
    gpgme \
    build-essential \
    && apt-get clean

# Set working directory
WORKDIR /app

# Copy requirements.txt first to leverage Docker layer caching
COPY requirements.txt .

# Install Python dependencies with pip3
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port your app will run on
EXPOSE 3002

# Command to run your Flask application
CMD ["python3", "src/server/stripe_server.py"]