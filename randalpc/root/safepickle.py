#!/usr/bin/env python3

import sys
import json


def log(*data, fnc="print"):
    print_fnc = eval(fnc)
    print_fnc(*data)


def has_key(obj, key):
    try:
        getattr(obj, key)
        return True
    except AttributeError:
        return False


class SafePickleNode:
    def __str__(self) -> str:
        res = []
        v = vars(self)
        for k in v:
            res.append(f"{k}: {v[k]}")
        return "(" + ", ".join([str(x) for x in res]) + ")"


if len(sys.argv) != 2:
    log("Usage: safepickle <filetodecode>")
    exit(1)

log("Trying to decode file " + sys.argv[1])

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()

obj = SafePickleNode()
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
        if type(curr) == dict:
            if not curr_key in parent:
                parent[curr_key] = SafePickleNode()
            curr = parent[curr_key]
        else:
            if not has_key(curr, curr_key):
                curr = SafePickleNode()
                setattr(parent, curr_key, curr)
            else:
                curr = getattr(parent, curr_key)
    elif cmd == "S":
        # String
        if type(parent) == dict:
            parent[curr_key] = lines.pop(0)
        else:
            setattr(parent, curr_key, lines.pop(0))
    elif cmd == "I":
        # Integer
        if type(parent) == dict:
            parent[curr_key] = int(lines.pop(0))
        else:
            setattr(parent, curr_key, int(lines.pop(0)))
    else:
        log("Unknown command", cmd)
        exit(1)

print("SUCCESSFULLY DECODED:", obj)

log("Finished!")
