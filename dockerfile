# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Prevent Python from writing .pyc files and ensure output is sent straight to terminal
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies and PostgreSQL client libraries
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements file and install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . /

# Expose port 8000 for the application
EXPOSE 8000

# Run database migrations and start Gunicorn server
CMD python manage.py migrate && gunicorn cribhunt.wsgi:application --bind 0.0.0.0:8000
