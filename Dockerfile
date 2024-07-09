# Use the official Python image with tag 3.9-slim as base image
FROM python:3.9-slim

# Set environment variable to prevent buffering of Python output
ENV PYTHONUNBUFFERED 1

# Set working directory inside the container
WORKDIR /klarian

# Copy the requirements.txt file from your host to the container's working directory
COPY requirements.txt .

# Install Python dependencies from requirements.txt
RUN pip install -r requirements.txt

# Copy the entire current directory from your host to the container's working directory
COPY . /klarian/
