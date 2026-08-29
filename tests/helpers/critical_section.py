#!/usr/bin/env python3
"""Small locked counter used by the concurrency stress tests."""

import fcntl
import json
import os
import sys
import time
from pathlib import Path


state_path = Path(sys.argv[1])
duration = float(sys.argv[2])
label = sys.argv[3]

state_path.parent.mkdir(parents=True, exist_ok=True)
with state_path.open("a+", encoding="utf-8") as handle:
    fcntl.flock(handle, fcntl.LOCK_EX)
    handle.seek(0)
    raw = handle.read().strip()
    state = json.loads(raw) if raw else {"active": 0, "max": 0, "starts": [], "ends": []}
    state["active"] += 1
    state["max"] = max(state["max"], state["active"])
    state["starts"].append(label)
    handle.seek(0)
    handle.truncate()
    json.dump(state, handle)
    handle.flush()
    os.fsync(handle.fileno())
    fcntl.flock(handle, fcntl.LOCK_UN)

time.sleep(duration)

with state_path.open("r+", encoding="utf-8") as handle:
    fcntl.flock(handle, fcntl.LOCK_EX)
    state = json.load(handle)
    state["active"] -= 1
    state["ends"].append(label)
    handle.seek(0)
    handle.truncate()
    json.dump(state, handle)
    handle.flush()
    os.fsync(handle.fileno())
