#!/bin/bash

if [ $# -lt 1 ]; then
    echo "usage: $0 <dir>"
    exit 1
fi

start_dir=$(pwd)
dirname=$1

cd $dirname
wc $(ls) | tail -n 1 | sed -E 's/^ +//' | cut -d' ' -f 1
cd $start_dir
