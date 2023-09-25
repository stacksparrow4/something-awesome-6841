#!/bin/bash

wc $(ls) | tail -n 1 | sed -E 's/^ +//' | cut -d' ' -f 1
