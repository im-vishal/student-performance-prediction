# End to End ML Project: Student Performance Prediction

The objective of the project is to learn about end-to-end project implementation which includes following steps
- ML Project Structure (Python Packaging & Modular Coding)
- Custom Exception handling, logging of information
- Create DVC stages with DagsHub & MLflow integration for experiment tracking:
    - Data Ingestion Stage
    - Data Transformation Stage
    - Train Model Stage
    - Model Registration (MLflow) Stage
- Use AWS S3 as DVC remote storage
- Hyperparameter tuning from `params.yaml` file
- Staging to Production movement of best model
- FastAPI to serve API
- Dockerization of project
- CI-CD pipeline
    - GitHub Actions, Workflows
    - GitHub self-hosted runners
- Deployment on AWS
    - DockerHub to EC2 (Single) Deployment
    - ECR to EC2 (Single) Deployment
    - Scalable deployment through below AWS Services:
        - Launch Templates
        - Auto Scaling Group (ASG)
        - Elastic Load Balancers
        - Target Groups
        - Amazon Machine Image (AMI)



## IMP CLI Commands for reference
### Docker flow

- docker build -t virtualvishal/st-score1 .
- sudo chmod 666 /var/run/docker.sock
- docker run -p 8888:8080 -e DAGSHUB_PAT=c52d45d06347759d028fabbb3cc57e53cf6d5a33 virtualvishal/st-score1
- docker ps
- docker login
- docker push virtualvishal/st-score1:v1.1

### Manual

- create an ec2 instance
- sudo apt-get update
- sudo apt-get install -y docker.io
- sudo systemctl start docker
- sudo systemctl enable docker
- sudo docker pull virtualvishal/st-score2:latest
- sudo docker run -p 80:8080 -e DAGSHUB_PAT=c52d45d06347759d028fabbb3cc57e53cf6d5a33 virtualvishal/st-score2:latest
- AWS Securtiy group

### CICD Flow with DockerHub
- create an ec2 instance
- sudo apt-get update
- sudo apt-get install -y docker.io
- sudo systemctl start docker
- sudo systemctl enable docker
- sudo usermod -aG docker $USER
- exit
- docker ps (new connection)
- add secrets to GitHub
    - EC2_HOST
    - EC2_USER
    - EC2_SSH_KEY
- modify ci.yaml
- push
- AWS security group

### run docker image in ecr
- aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 823558662715.dkr.ecr.ap-south-1.amazonaws.com
- docker build -t virtualvishal .
- docker tag virtualvishal:latest 823558662715.dkr.ecr.ap-south-1.amazonaws.com/virtualvishal:v1.4
- docker push 823558662715.dkr.ecr.ap-south-1.amazonaws.com/virtualvishal:v1.4
- Open new terminal
- docker pull 823558662715.dkr.ecr.ap-south-1.amazonaws.com/virtualvishal:v1.4
- docker run -d -p 8888:8080 --name my-app 823558662715.dkr.ecr.ap-south-1.amazonaws.com/virtualvishal:v1.4 (wrong method dagshub_pat not set)
- docker stop my-app
- docker rm my-app
- docker run -d -p 8888:8080 -e DAGSHUB_PAT=c52d45d06347759d028fabbb3cc57e53cf6d5a33 --name my-app 823558662715.dkr.ecr.ap-south-1.amazonaws.com/virtualvishal:v1.4


### CICD Flow with ECR
- setup ec2 machine
- sudo apt-get update
- sudo apt-get install -y docker.io
- sudo systemctl start docker
- sudo systemctl enable docker
- sudo apt-get update
- sudo apt-get install -y unzip curl
- curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
- unzip awscliv2.zip
- sudo ./aws/install
- sudo usermod -aG docker ubuntu
- aws configure
- aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 823558662715.dkr.ecr.ap-south-1.amazonaws.com
- docker pull 823558662715.dkr.ecr.ap-south-1.amazonaws.com/virtualvishal:v1.4
- docker run -d -p 8888:8080 -e DAGSHUB_PAT=c52d45d06347759d028fabbb3cc57e53cf6d5a33 --name my-app 823558662715.dkr.ecr.ap-south-1.amazonaws.com/virtualvishal:v1.4

### CICD with ECR and EC2 deployment
- create ec2
- setup
    - setup ec2 machine
    - sudo apt-get update
    - sudo apt-get install -y docker.io
    - sudo systemctl start docker
    - sudo systemctl enable docker
    - sudo apt-get update
    - sudo apt-get install -y unzip curl
    - curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    - unzip awscliv2.zip
    - sudo ./aws/install
    - sudo usermod -aG docker ubuntu
    - exit then next
- add pem file as secret key to Github Secrets
- add deployment stage in ci.yaml
- commit and push
- add security group

### squash commits
- git switch -c test-branch
- git add .
- git commit -m "test1"
- git push origin test-branch
- git checkout test-branch
- git rebase -i main
    * pick f7c8a8a Test commit 1
    * squash d3b5746 Test commit 2
    * squash a6d5fa1 Test commit 3
- git switch main
- git merge -ff-only test-branch
- git push origin main
- git branch -d test-branch
- git push origin --delete test-branch


### steps for CodeDeploy Manual Deployment

- create a new launch template
    - create a new IAM role - EC2_Codedeploy_role -> policy - Amazon EC2RoleforAWSCodeDeploy - create a new IAM role - EC2_ECR_role -> policy - Amazon EC2ContainerRegistryReadOnly
    - install and codedeploy agent in using User data
******************************************************************************************************************************

Use code from launch template in user data.

*******************************************************************************************************************************

- create a new ASG using the above launch template
- check if codedeploy agent is running - sudo service codedeploy-agent status
- create a new codedeploy application
- create a deployment group -> Service role -> CodeDeployServiceRole -> AWSCodeDeployRole
- add files to your project repo -> get GitHub token
- create new deployment
- monitor the deployment
- check the docker application
