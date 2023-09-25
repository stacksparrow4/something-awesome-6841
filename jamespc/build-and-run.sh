#!/bin/bash

docker build -t jamespc .
docker run --cap-add LINUX_IMMUTABLE --rm -it -p 1337:80 -p 2222:22 jamespc
