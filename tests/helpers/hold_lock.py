#!/usr/bin/env python3
"""Hold an existing flock until terminated, for lock-wait tests."""

import fcntl
import signal
import sys
import time
from pathlib import Path

lock_path = Path(sys.argv[1])
ready_path = Path(sys.argv[2])
stopping = False


def stop(_signum: int, _frame: object) -> None:
    global stopping
    stopping = True


signal.signal(signal.SIGTERM, stop)
with lock_path.open("r+") as lock:
    fcntl.flock(lock, fcntl.LOCK_EX)
    ready_path.touch()
    while not stopping:
        time.sleep(0.01)
