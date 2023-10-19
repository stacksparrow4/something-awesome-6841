#!/bin/bash

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <url>"
    exit 1
fi

triggerbot.sh 9e8022da832dbc0d2e09be5c9441e54d31ed39a18d34b0a9e853ed1c2205457a "$1"
