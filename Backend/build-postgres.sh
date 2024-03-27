#!/bin/bash

Network="colab-platform-local"

docker build -f Dockerfile.postgres -t postgres-image .

docker run --rm -p 5050:5432  --name=postgres_test --network=$Network -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=1234 \
    -v postgres_data:/home/abhijit/postgres -d postgres-image 

export PGPASSWORD='1234' psql -h localhost -p 5432 -U postgres -c create database "platform_data"