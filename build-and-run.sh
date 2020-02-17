#!/bin/bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR

#./copy-photos

#./build-docker.sh
docker run --network=host --rm -v `pwd`/app:/app -v `pwd`/webpage:/webpage -w /webpage photoweb run build

./run-server.sh
