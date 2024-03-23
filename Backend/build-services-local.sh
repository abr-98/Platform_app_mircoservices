#!/bin/bash

if [$# -lt 3]; then
    echo "Please provide the following
    1. Service Name
    2. Docker File"
    3. Port
    exit
else
    Service=$1
    DockerFile=$2
    Port=$3
    Network="colab-platform-local"

    echo "Using Service $Service"
fi

if test $(docker ps -a -q --filter "name=$Service"); then
    echo "Stopping and removing container"
    docker stop $Service
    docker rm -f $Service
fi

docker build -f $DockerFile -t $Service-image .

docker run -p $Port:5000  --name=$Service --network=$Network -d $Service-image 


