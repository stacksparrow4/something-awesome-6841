#!/bin/bash

docker build -t jamespc .
docker run --rm -it -p 1337:80 -p 2222:22 jamespc
