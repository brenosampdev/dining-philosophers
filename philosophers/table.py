"""Table with the forks and the salt shaker that controls who may pick them up."""

import itertools
import threading

from .log import log


class SaltShaker:
    """
    Single resource on the table: only whoever holds the salt shaker may pick up forks.

    It works as a ticket queue (ticket lock): whoever asks for the salt shaker gets
    a ticket and only receives it when that ticket is called. A plain
    threading.Lock does not guarantee arrival order, so a philosopher could lose
    their turn forever.
    """

    def __init__(self):
        self.cond = threading.Condition()
        self.next_ticket = itertools.count()
        self.called_ticket = 0

    def take(self):
        with self.cond:
            ticket = next(self.next_ticket)
            # wait_for releases the lock while waiting and reacquires it on wake up.
            self.cond.wait_for(lambda: self.called_ticket == ticket)

    def give_back(self):
        with self.cond:
            self.called_ticket += 1
            self.cond.notify_all()      # wakes everyone; only the next ticket holder proceeds


class Table:
    """The 5 forks (one Lock each) and the shared salt shaker."""

    def __init__(self, n):
        self.n = n
        self.forks = [threading.Lock() for _ in range(n)]  # fork i sits between philosopher i and i+1
        self.salt_shaker = SaltShaker()

    def forks_of(self, i):
        # Left fork = i, right fork = (i + 1) % n
        return i, (i + 1) % self.n

    def take_salt_shaker(self, i):
        self.salt_shaker.take()
        log(f"[Philosopher {i}] Took the salt shaker.")

    def return_salt_shaker(self, i):
        self.salt_shaker.give_back()
        log(f"[Philosopher {i}] Returned the salt shaker.")

    def take_forks(self, i):
        # Only called by whoever holds the salt shaker, and the salt shaker is only
        # returned after the meal: the forks are always free here -> no circular wait.
        left, right = self.forks_of(i)
        self.forks[left].acquire()
        self.forks[right].acquire()

    def return_forks(self, i):
        left, right = self.forks_of(i)
        self.forks[right].release()
        self.forks[left].release()
