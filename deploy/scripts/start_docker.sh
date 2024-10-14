#!/bin/bash
# Login to AWS ECR
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 823558662715.dkr.ecr.ap-south-1.amazonaws.com

# Pull the latest image
docker pull 823558662715.dkr.ecr.ap-south-1.amazonaws.com/virtualvishal:latest

# Check if the container 'campusx-app' is running
if [ "$(docker ps -q -f name=st-score-app)" ]; then
    # Stop the running container
    docker stop st-score-app
fi

# Check if the container 'campusx-app' exists (stopped or running)
if [ "$(docker ps -aq -f name=st-score-app)" ]; then
    # Remove the container if it exists
    docker rm st-score-app
fi

# Run a new container
docker run -d -p 80:8080 -e DAGSHUB_PAT=c52d45d06347759d028fabbb3cc57e53cf6d5a33 --name st-score-app 823558662715.dkr.ecr.ap-south-1.amazonaws.com/virtualvishal:latest