#!/usr/bin/env python3

import sys
import json


def log(data, fnc="print"):
    print_fnc = eval(fnc)
    print_fnc(data)


if len(sys.argv) != 2:
    log("Usage: safepickle <filetodecode>")
    exit(1)

log("Trying to decode file " + sys.argv[1])

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()

obj = {}
parent = None
curr = obj
curr_key = None

while len(lines) > 0:
    cmd = lines.pop(0)
    if cmd == "R":
        # Reset
        parent = None
        curr = obj
        curr_key = None
    elif cmd == "K":
        # Key
        curr_key = lines.pop(0)
        parent = curr
        curr[curr_key] = {}
        curr = curr[curr_key]
    elif cmd == "S":
        # String
        parent[curr_key] = lines.pop(0)
    elif cmd == "I":
        # Integer
        parent[curr_key] = int(lines.pop(0))
    else:
        log("Unknown command", cmd)
        exit(1)

print("SUCCESSFULLY DECODED:", json.dumps(obj, indent=2))

log("Finished!")
