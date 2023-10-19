#!/bin/bash

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <url>"
    exit 1
fi

triggerbot.sh c8b65101957f50df0984322aecced18597d417f3970fce4b113037e646855f4c "$1"
