# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install pipenv
RUN pip install pipenv

# Copy Pipfile and Pipfile.lock into the container
COPY Pipfile Pipfile.lock ./

# Install dependencies via pipenv
RUN pipenv install --deploy

# Copy the rest of the application code into the container
COPY . .

# Define the command to run the script
CMD ["pipenv", "run", "python", "./check_ssl.py"]
