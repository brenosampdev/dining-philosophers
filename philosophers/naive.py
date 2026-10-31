"""Naive version (one mutex per fork) used to demonstrate the deadlock."""

import random
import threading
import time

from .config import NUM_PHILOSOPHERS
from .log import log


def run_naive(deadlock_timeout):
    """
    Version WITHOUT any handling: each philosopher picks up the left fork and then
    the right one, with one Lock per fork. The pause between the two "acquire"
    calls forces everyone to hold the left fork at the same time -> circular
    wait -> deadlock.
    """
    log("=== NAIVE version (one mutex per fork, no ordering) ===")
    forks = [threading.Lock() for _ in range(NUM_PHILOSOPHERS)]
    progress = [0]

    def philosopher(i):
        left, right = i, (i + 1) % NUM_PHILOSOPHERS
        while True:
            log(f"[Philosopher {i}] Started thinking.")
            time.sleep(random.uniform(0.1, 0.3))
            log(f"[Philosopher {i}] Trying to pick up forks {left} (left) and {right} (right)...")
            forks[left].acquire()
            log(f"[Philosopher {i}] Picked up the left fork ({left}), waiting for the right one ({right})...")
            time.sleep(0.5)             # window that makes the deadlock practically certain
            forks[right].acquire()
            log(f"[Philosopher {i}] Got the forks and started eating.")
            progress[0] += 1
            time.sleep(random.uniform(0.1, 0.3))
            forks[right].release()
            forks[left].release()
            log(f"[Philosopher {i}] Finished eating and put down the forks.")

    for i in range(NUM_PHILOSOPHERS):
        threading.Thread(target=philosopher, args=(i,), daemon=True).start()

    # "Watchdog": if nobody eats for deadlock_timeout seconds, we are stuck.
    last, since = progress[0], time.monotonic()
    while True:
        time.sleep(0.2)
        if progress[0] != last:
            last, since = progress[0], time.monotonic()
        elif time.monotonic() - since > deadlock_timeout:
            log(f"!!! DEADLOCK: no philosopher has eaten in the last {deadlock_timeout}s. "
                "Everyone holds the left fork and waits for the right one (circular wait).")
            return
