"""Runs the correct solution (salt shaker) and prints the final report."""

import threading
import time

from .config import NUM_PHILOSOPHERS
from .log import log, print_lock
from .philosopher import Philosopher
from .table import Table


def run_solution(duration):
    log(f"=== Salt shaker solution ({NUM_PHILOSOPHERS} philosophers, {duration}s) ===")
    table = Table(NUM_PHILOSOPHERS)
    stop = threading.Event()
    philosophers = [Philosopher(i, table, stop) for i in range(NUM_PHILOSOPHERS)]

    for p in philosophers:
        p.start()
    time.sleep(duration)
    stop.set()                          # each thread exits at the end of its current cycle
    for p in philosophers:
        p.join()

    log("=== End of run: all threads finished (no deadlock) ===")
    print_report(philosophers)


def print_report(philosophers):
    with print_lock:
        print("\nPhilosopher | Meals | Avg wait (s) | Longest wait (s)")
        print("-" * 55)
        for p in philosophers:
            avg = p.total_wait / p.meals if p.meals else 0.0
            print(f"{p.id:^11} | {p.meals:^5} | {avg:^12.2f} | {p.longest_wait:^16.2f}")
        total = sum(p.meals for p in philosophers)
        print(f"\nTotal meals: {total}. Everyone ate: "
              f"{'YES' if all(p.meals > 0 for p in philosophers) else 'NO'}")
