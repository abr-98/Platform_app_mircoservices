#!/bin/bash
networkName = "colab-platform-local"

echo "creating network $networkName"
if ! test $(docker network ls -q --filter "name=$networkName"); then
    docker network create --driver=bridge --attachable=true $networkName
fi