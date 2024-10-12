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

# CICD Flow
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