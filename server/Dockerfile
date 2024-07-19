# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Pipenv
RUN pip install pipenv

# Copy Pipfile and Pipfile.lock to the working directory
COPY Pipfile Pipfile.lock /app/

# Install dependencies
RUN pipenv install --deploy --ignore-pipfile

# Copy the current directory contents into the container at /app
COPY . /app

# Expose port 5000 (the default port for Flask)
EXPOSE 5000

# Run the Flask application
CMD ["pipenv", "run", "gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
