#!/bin/bash

# This executable is used to build docker image locally
set -e

[[ -f .env ]] && source .env

export APP_NAME=flask-api
export REVIEW_SLOT=1
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity | jq .Account -r)
export IMAGE_REPO_NAME=$APP_NAME
export SOURCE_BRANCH=$(git branch | grep "*" | sed s/\*\ //g)
export USE_REMOTE_DOCKER_CACHE=false
export SKIP_UPLOAD_CACHE=true
export DOCKER_FILE=./Dockerfile 
export FETCH_AWS_SECRETS=false
export FETCH_REPO_VERSION=false
export ECR_LOGIN=false

# Project ARGS
export PYTHON_VERSION=3.9.5
export PYTHON_COMMAND=3.9


export BUILD_CONTEXT=../..
cd $BUILD_CONTEXT
./docker/codebuild/codebuild.sh

# Clean up

# docker image prune -f > /dev/null 2>&1
# docker image ls | grep "<none>" | awk '{print $3}' | xargs docker image rm -f > /dev/null 2>&1
