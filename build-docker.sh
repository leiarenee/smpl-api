#!/bin/bash

docker build . -t smpl-api --build-arg PYTHON_VERSION=3.9.5 --build-arg PYTHON_COMMAND=3.9
