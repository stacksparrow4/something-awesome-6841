#!/bin/bash

docker build -t randalpc .
docker run --rm -it -p 1337:80 -p 2222:22 randalpc
