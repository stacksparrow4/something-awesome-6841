#!/bin/bash

gcc -m32 -fno-stack-protector -masm=intel -no-pie funprogram.c -o funprogram
