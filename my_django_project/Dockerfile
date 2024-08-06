# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /usr/src/app

# Install dependencies
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt --break-system-packages

# Copy project files
COPY . /usr/src/app/

# Expose the port the app runs on
EXPOSE 8000

# Command to run on container start
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]
