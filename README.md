# Dining Philosophers

This project is a Python implementation of the classic Dining Philosophers problem, developed for the Operating Systems course. It shows how careless use of locks leads to a deadlock and how a simple coordination rule removes both deadlock and starvation.

## The problem

Five philosophers sit around a round table. Between each pair of neighbors there is a single fork, so the table has five forks in total. Each philosopher spends their life alternating between thinking and eating, and to eat they need both the fork on their left and the fork on their right. The challenge is to design a protocol that lets every philosopher eat without the system freezing and without any philosopher being left hungry forever.

If every philosopher picks up the left fork and then waits for the right one, it is possible that all five grab their left fork at the same moment. Each one then waits for a fork that is held by a neighbor who is also waiting, forming a circular wait. Nobody can continue and the program stops making progress. This situation is called a deadlock.

## The solution: a salt shaker

The solution adds a single salt shaker to the table. A philosopher is only allowed to pick up forks while holding the salt shaker. The philosopher who holds it takes both forks, eats, puts the forks back and only then returns the salt shaker. Because only one philosopher at a time can be touching forks, the circular wait can never form, which means deadlock is impossible.

Avoiding deadlock is not enough on its own, because a plain lock in Python does not guarantee that waiting threads are served in order of arrival. An unlucky philosopher could keep losing the race and never eat, which is called starvation. To prevent this, the salt shaker is handed out through a ticket queue. Whoever asks for it receives a ticket number, and the salt shaker is passed along strictly by ticket order. Whoever asked first is served first, so every philosopher is guaranteed to eat eventually.

The trade off of this approach is reduced parallelism. Only one philosopher eats at a time, even though in theory two non adjacent philosophers could eat simultaneously. For this assignment the priority is correctness and fairness, and the design keeps the reasoning about safety very simple.

## Project structure

The entry point is `dining_philosophers.py`, which reads the command line options and chooses which version to run. The rest of the code lives in the `philosophers` package.

The file `config.py` holds the shared constants, such as the number of philosophers. The file `log.py` provides a thread safe logging function that prefixes every message with the elapsed time and prevents lines from different threads from mixing in the console. The file `table.py` defines the `SaltShaker` class, which implements the ticket queue on top of a `threading.Condition`, and the `Table` class, which owns the forks (one `threading.Lock` per fork) and the salt shaker. The file `philosopher.py` defines the `Philosopher` thread, which loops through thinking, waiting for the salt shaker, eating and returning everything, while collecting statistics about meals and waiting time. The file `solution.py` starts the philosophers, lets them run for the requested time, stops them cleanly and prints a final report. The file `naive.py` contains the naive version with one lock per fork and no coordination, used to demonstrate the deadlock.

## Running

The project uses only the Python standard library, so no installation is needed beyond Python 3. To run the correct solution for the default duration of 30 seconds, use the command below.

```
python dining_philosophers.py
```

To choose a different duration, pass the number of seconds with the duration option.

```
python dining_philosophers.py --duration 60
```

To see the deadlock happen, run the naive version.

```
python dining_philosophers.py --naive
```

## What to expect

When running the solution, the console shows each philosopher thinking, trying to pick up forks, taking the salt shaker, eating and returning everything. At the end, a table reports for every philosopher how many meals they had, their average waiting time and their longest wait. The last line confirms whether every philosopher managed to eat at least once, which demonstrates the absence of starvation, and the fact that all threads finish cleanly demonstrates the absence of deadlock.

When running the naive version, every philosopher quickly picks up their left fork and waits for the right one. A watchdog monitors progress, and if no philosopher eats for three seconds it reports the deadlock and explains that every philosopher is holding the left fork while waiting for the right one.

## Report

The file `Relatorio Jantar dos Filosofos - final.pdf` contains the full written report for the assignment, with the theoretical discussion and the analysis of the results.
