docker build -t virtualvishal/st-score1 .

sudo chmod 666 /var/run/docker.sock

docker run -p 8888:8080 -e DAGSHUB_PAT=c52d45d06347759d028fabbb3cc57e53cf6d5a33 virtualvishal/st-score1

docker ps

docker login

docker push virtualvishal/st-score1:v1.1

