"""Thread that represents a philosopher using the Table (forks + salt shaker)."""

import random
import threading
import time

from .log import log


class Philosopher(threading.Thread):

    def __init__(self, id_, table, stop, think=(0.5, 2.0), eat=(0.5, 1.5)):
        super().__init__(name=f"Philosopher-{id_}", daemon=True)
        self.id = id_
        self.table = table
        self.stop = stop
        self.think_range = think
        self.eat_range = eat
        self.meals = 0
        self.longest_wait = 0.0
        self.total_wait = 0.0
        left, right = table.forks_of(id_)
        self.fork_names = f"{left} (left) and {right} (right)"

    def think(self):
        log(f"[Philosopher {self.id}] Started thinking.")
        time.sleep(random.uniform(*self.think_range))

    def eat(self):
        log(f"[Philosopher {self.id}] Got forks {self.fork_names} and started eating.")
        time.sleep(random.uniform(*self.eat_range))

    def run(self):
        while not self.stop.is_set():
            self.think()

            log(f"[Philosopher {self.id}] Trying to pick up forks {self.fork_names}...")
            t0 = time.monotonic()
            self.table.take_salt_shaker(self.id)   # the others wait until it is returned
            wait = time.monotonic() - t0
            self.total_wait += wait
            self.longest_wait = max(self.longest_wait, wait)

            self.table.take_forks(self.id)
            self.eat()
            self.meals += 1

            self.table.return_forks(self.id)
            log(f"[Philosopher {self.id}] Finished eating and put down forks {self.fork_names}.")
            self.table.return_salt_shaker(self.id)
