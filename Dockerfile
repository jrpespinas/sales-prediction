# syntax=docker/dockerfile:1
FROM python:3.10.10-alpine

# Set current work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the package
COPY . . 

# Expose container port (locally)
# Comment out for heroku deployment, as it does not need it
# EXPOSE 8080

# Run the backend in heroku
CMD ["./start.sh"]