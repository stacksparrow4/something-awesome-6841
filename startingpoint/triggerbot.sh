#!/bin/bash

if [[ $# -ne 2 ]]; then
    echo "Usage: $0 <runhash> <relurl>"
    exit 1
fi

if ! grep -qE '^https?://[A-Za-z.:0-9-]+/' <<< "$2"; then
    echo "Incorrectly formatted url. Format url like follows: http://stacksparrow4.xyz:9001/mypost"
    exit 1
fi

url=$(sed -E 's/^https?:\/\/[A-Za-z.:0-9-]+\///' <<< "$2" | sed 's/"/\"/')
curl -X POST http://xssbot:1337/visit -H 'Content-Type: application/json' -d "{\"runHash\": \"$1\", \"url\": \"$url\"}"
