"""Volume 10, Chapter 3 - Proving Greedy Correct: Exchange Arguments and Staying Ahead.

Run:  python3 ch03_examples.py
"""

from __future__ import annotations

import itertools


def total_waiting(durations: list[int], order: list[int]) -> int:
    """Sum of every customer's waiting time (time until their own service finishes)."""
    clock = total = 0
    for i in order:
        clock += durations[i]
        total += clock
    return total


def shortest_first(durations: list[int]) -> list[int]:
    """Greedy: serve the shortest job first. Exchange argument: swapping any longer-before-shorter pair helps."""
    return sorted(range(len(durations)), key=lambda i: durations[i])


def max_lateness(jobs: list[tuple[int, int]], order: list[int]) -> int:
    """jobs[i] = (duration, deadline). Lateness = finish - deadline (0 if on time). Return the worst."""
    clock = worst = 0
    for i in order:
        clock += jobs[i][0]
        worst = max(worst, clock - jobs[i][1])
    return worst


def earliest_deadline_first(jobs: list[tuple[int, int]]) -> list[int]:
    """Greedy: do jobs in deadline order. An 'inversion' (later deadline before earlier) can be swapped without
    increasing the maximum lateness - so some optimal schedule has no inversions, i.e. is EDF."""
    return sorted(range(len(jobs)), key=lambda i: jobs[i][1])


def brute_best(n: int, score) -> int:
    """Reference: try every order (n!)."""
    return min(score(list(p)) for p in itertools.permutations(range(n)))


def stays_ahead_activities(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Greedy for 'most non-overlapping events': always take the event that ENDS earliest.
    Stays-ahead argument: after k picks, greedy's k-th end time is never later than any other plan's."""
    chosen, last_end = [], float("-inf")
    for s, e in sorted(intervals, key=lambda iv: iv[1]):
        if s >= last_end:
            chosen.append((s, e))
            last_end = e
    return chosen


def bank_queue_plan(service_minutes: dict[str, int]) -> tuple[list[str], int]:
    """Industry example: a bank teller with several customers - order to minimise total waiting."""
    names = list(service_minutes)
    durations = [service_minutes[n] for n in names]
    order = shortest_first(durations)
    return [names[i] for i in order], total_waiting(durations, order)


if __name__ == "__main__":
    d = [5, 1, 3]
    print("SJF order:", shortest_first(d), "waiting", total_waiting(d, shortest_first(d)),
          "| best possible", brute_best(3, lambda o: total_waiting(d, o)))
    jobs = [(3, 6), (2, 8), (1, 9), (4, 9), (3, 14), (2, 15)]
    edf = earliest_deadline_first(jobs)
    print("EDF max lateness:", max_lateness(jobs, edf), "| best", brute_best(len(jobs), lambda o: max_lateness(jobs, o)))
    print("events:", stays_ahead_activities([(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 11)]))
    print("bank:", bank_queue_plan({"Asha": 8, "Bilal": 2, "Chen": 5}))
