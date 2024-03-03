# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . /app/

# Create directory for the database
RUN mkdir -p /app/app/data

# Set permissions for the directory (optional)
RUN chmod 777 /app/app/data

# Run the application
RUN python init_db.py

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:create_app()"]