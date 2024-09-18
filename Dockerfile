# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install Git (necessary to clone from GitHub)
RUN apt-get update && apt-get install -y git

# Clone the repository from GitHub
RUN git clone https://github.com/muruganpm/pythonapp.git .

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Command to run the application
CMD ["python", "app.py"]
