#!/bin/bash
set -e
echo "Flask API Server"
if [ $1 == "test" ]
then
  ./pyrun.sh docker-test
else
  exec "$@"
fi