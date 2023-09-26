#!/bin/bash

docker build -t xssbot .
docker run --rm -it -p 1337:1337 xssbot
