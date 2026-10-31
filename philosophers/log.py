"""Thread safe console output."""

import threading
import time

# Lock used only so that console lines from different threads do not interleave.
print_lock = threading.Lock()
_start = time.monotonic()


def log(msg):
    with print_lock:
        print(f"[{time.monotonic() - _start:7.2f}s] {msg}", flush=True)
