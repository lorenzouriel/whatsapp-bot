# Use the official Python image as the base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY src/ ./src/

# Expose the port the app runs on
EXPOSE 5000

# Set the default command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "src.app:app"]