#!/usr/bin/env python3
"""Signal-aware child used to verify forwarding."""

import os
import signal
import sys
import time
from pathlib import Path


ready = Path(sys.argv[1])
received = Path(sys.argv[2])


def stop(signum: int, _frame: object) -> None:
    received.write_text(str(signum), encoding="ascii")
    raise SystemExit(128 + signum)


signal.signal(signal.SIGTERM, stop)
signal.signal(signal.SIGINT, stop)
ready.write_text(str(os.getpid()), encoding="ascii")
while True:
    time.sleep(1)
