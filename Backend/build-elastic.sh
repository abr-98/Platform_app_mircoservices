#!/bin/bash
Network="colab-platform-local"

docker build -f Dockerfile.elastic -t elastic-image .

docker run --rm -p 9200:9200 -p 9300:9300  --name=elastic_test --network=$Network -e "discovery.type=single-node" \
    -e "xpack.security.enabled=false" -d elastic-image 