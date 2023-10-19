#!/bin/bash

actualpath=$(realpath $1)
if [[ "$actualpath" = "/usr/local/bin/healthcheck.sh" ]] && [ -O "$1" ]; then
    "$1"
else
    echo "NOPE"
fi
