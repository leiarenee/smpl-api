#!/bin/bash
set -e
/usr/bin/xray -t 0.0.0.0:2000 -b 0.0.0.0:2000 -o -n eu-central-1 &

echo "Flask API Server"
if [ $1 == "test" ]
then
  ./pyrun.sh docker-test
else
  exec "$@"
fi