# Base image, assuming you're using a Python Flask app
FROM python:3.11-slim

# Set environment variables to ensure Python runs in unbuffered and non-interactive mode
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libgpgme-dev \
    gpg \
    && apt-get clean

# Create and set working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Expose the port Flask will run on
EXPOSE 3002

# Set environment variables for Flask
ENV FLASK_APP=src/server/stripe_server.py
ENV FLASK_ENV=production

# Command to run the Flask app
CMD ["python", "src/server/stripe_server.py"]
