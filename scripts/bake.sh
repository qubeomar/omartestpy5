#!/bin/bash
set -o allexport

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/..

if [ -e .env ]; then
	source .env
fi
echo $OMARTESTPY5_DOCKER_IMAGE_LOCAL

docker build -t $OMARTESTPY5_DOCKER_IMAGE_LOCAL:$OMARTESTPY5_IMAGE_VERSION . 
