"""
Dining Philosophers, Operating Systems

Solution with a SALT SHAKER: a single salt shaker on the table, handed out in
order of arrival.

  * Each philosopher is a thread (threading.Thread) and each fork is a Lock.
  * Before picking up the forks, a philosopher must take the salt shaker. Whoever
    holds the salt shaker picks up both forks, eats, puts the forks back and only
    then returns the salt shaker; meanwhile, the others wait.
  * Since only one philosopher at a time holds forks, the cycle of "everyone
    holds the left fork and waits for the right one" never forms -> no deadlock.
  * The salt shaker is handed out by ticket (FIFO queue): whoever asked first is
    served first, so nobody goes hungry forever -> no starvation.

Structure:
    philosophers/config.py       constants (number of philosophers)
    philosophers/log.py          thread safe console logging
    philosophers/table.py        Table (forks) and SaltShaker (ticket queue)
    philosophers/philosopher.py  Philosopher thread
    philosophers/solution.py     runs the correct solution + report
    philosophers/naive.py        naive version that demonstrates the deadlock

Usage:
    python dining_philosophers.py                  # correct solution, 30 s
    python dining_philosophers.py --duration 60    # runs for 60 s
    python dining_philosophers.py --naive          # naive version, shows deadlock
"""

import argparse

from philosophers.naive import run_naive
from philosophers.solution import run_solution


def main():
    parser = argparse.ArgumentParser(description="Dining Philosophers")
    parser.add_argument("--duration", type=float, default=30,
                        help="seconds to run the solution (default: 30)")
    parser.add_argument("--naive", action="store_true",
                        help="runs the naive version to demonstrate the deadlock")
    args = parser.parse_args()

    if args.naive:
        run_naive(deadlock_timeout=3)
    else:
        run_solution(args.duration)


if __name__ == "__main__":
    main()
