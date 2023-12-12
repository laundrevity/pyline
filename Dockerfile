# Use the official Python 3.12 image as a parent image
FROM python:3.12

# Set the working directory in the Docker container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 81

# Define environment variable
ENV NAME World

ENTRYPOINT ["sleep", "infinity"]
