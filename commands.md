# Docker flow

docker build -t virtualvishal/st-score1 .

sudo chmod 666 /var/run/docker.sock

docker run -p 8888:8080 -e DAGSHUB_PAT=c52d45d06347759d028fabbb3cc57e53cf6d5a33 virtualvishal/st-score1

docker ps

docker login

docker push virtualvishal/st-score1:v1.1

# Manual

1. create an ec2 instance
2. sudo apt-get update
3. sudo apt-get install -y docker.io
4. sudo systemctl start docker
5. sudo systemctl enable docker
6. sudo docker pull virtualvishal/st-score2:latest
7. sudo docker run -p 80:8080 -e DAGSHUB_PAT=c52d45d06347759d028fabbb3cc57e53cf6d5a33 virtualvishal/st-score2:latest
8. AWS Securtiy group

# CICD Flow with DockerHub
1. create an ec2 instance
2. sudo apt-get update
3. sudo apt-get install -y docker.io
4. sudo systemctl start docker
5. sudo systemctl enable docker
6. sudo usermod -aG docker $USER
7. exit
8. docker ps (new connection)
9. add secrets to GitHub
    - EC2_HOST
    - EC2_USER
    - EC2_SSH_KEY
10. modify ci.yaml
11. push
12. AWS security group

# run docker image in ecr
1. aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 823558662715.dkr.ecr.ap-south-1.amazonaws.com
2. docker build -t virtualvishal .
3. docker tag virtualvishal:latest 823558662715.dkr.ecr.ap-south-1.amazonaws.com/virtualvishal:v1.4
4. docker push 823558662715.dkr.ecr.ap-south-1.amazonaws.com/virtualvishal:v1.4
5. Open new terminal
6. docker pull 823558662715.dkr.ecr.ap-south-1.amazonaws.com/virtualvishal:v1.4
7. docker run -d -p 8888:8080 --name my-app 823558662715.dkr.ecr.ap-south-1.amazonaws.com/virtualvishal:v1.4 (wrong method dagshub_pat not set)
8. docker stop my-app
9. docker rm my-app
10. docker run -d -p 8888:8080 -e DAGSHUB_PAT=c52d45d06347759d028fabbb3cc57e53cf6d5a33 --name my-app 823558662715.dkr.ecr.ap-south-1.amazonaws.com/virtualvishal:v1.4


# CICD Flow with ECR
1. setup ec2 machine
2. sudo apt-get update
3. sudo apt-get install -y docker.io
4. sudo systemctl start docker
5. sudo systemctl enable docker
6. sudo apt-get update
7. sudo apt-get install -y unzip curl
8. curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
9. unzip awscliv2.zip
10. sudo ./aws/install

11. sudo usermod -aG docker ubuntu
12. aws configure
13. aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 823558662715.dkr.ecr.ap-south-1.amazonaws.com
14. docker pull 823558662715.dkr.ecr.ap-south-1.amazonaws.com/virtualvishal:v1.4
15. docker run -d -p 8888:8080 -e DAGSHUB_PAT=c52d45d06347759d028fabbb3cc57e53cf6d5a33 --name my-app 823558662715.dkr.ecr.ap-south-1.amazonaws.com/virtualvishal:v1.4

# CICD with ECR and EC2 deployment
1. create ec2
2. setup
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
    - exit
3. add pem file as secret key to Github Secrets
4. add deployment stage in ci.yaml
5. commit and push
6. add security group

# squash commits
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