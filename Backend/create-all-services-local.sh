#!/bin/bash
sh build-services-local.sh status-service Dockerfile.Status 5000
sh build-services-local.sh user-service Dockerfile.User 5002
sh build-services-local.sh friend-service Dockerfile.Friend 5003
sh build-services-local.sh group-service Dockerfile.Group 5004
sh build-services-local.sh participant-service Dockerfile.Participant 5005