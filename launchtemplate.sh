#!/bin/bash
# Update the package list
sudo apt-get update -y

# Install Ruby (required by the CodeDeploy agent)
sudo apt-get install ruby -y

# Download the CodeDeploy agent installer from the correct region
wget https://aws-codedeploy-ap-south-1.s3.ap-south-1.amazonaws.com/latest/install

# Make the installer executable
chmod +x ./install

# Install the Code Deploy agent
sudo ./install auto

# Start the CodeDeploy agent
sudo service codedeploy-agent start