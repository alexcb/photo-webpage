#!/bin/bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR

./build-docker.sh
docker run --network=host --rm -ti -v `pwd`/webpage:/webpage -w /webpage photoweb run serve
