#!/usr/bin/env python3
"""Signal-aware child used to verify forwarding."""

import os
import signal
import sys
import time
from pathlib import Path

ready = Path(sys.argv[1])
received = Path(sys.argv[2])
encoded_signals = {
    int(signal.SIGTERM): str(int(signal.SIGTERM)).encode("ascii"),
    int(signal.SIGINT): str(int(signal.SIGINT)).encode("ascii"),
}


def stop(signum: int, _frame: object) -> None:
    fd = os.open(received, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    try:
        os.write(fd, encoded_signals[signum])
    finally:
        os.close(fd)
    raise SystemExit(128 + signum)


signal.signal(signal.SIGTERM, stop)
signal.signal(signal.SIGINT, stop)
ready.write_text(str(os.getpid()), encoding="ascii")
while True:
    time.sleep(0.05)
