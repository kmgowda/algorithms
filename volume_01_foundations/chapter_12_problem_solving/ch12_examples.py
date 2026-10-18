"""Chapter 12 - Thinking Like an Algorithm Designer: the SPIRAL method.

Each worked problem has a brute-force version and a refined version,
plus a stress tester that compares them on random inputs.

Run:  python3 ch12_examples.py
"""

from __future__ import annotations

import random
from typing import Callable


# ------------------------------------------------------------------ worked problem 1
# Missing ticket: tickets 0..n were sold, one is missing from the box. Which one?
def missing_ticket_brute(tickets: list[int]) -> int:
    """O(n^2): for every possible number, scan the list (hidden loop in `in`)."""
    for number in range(len(tickets) + 1):
        if number not in tickets:
            return number
    raise ValueError("nothing missing")


def missing_ticket_set(tickets: list[int]) -> int:
    """O(n) time, O(n) space: put the tickets in a set first."""
    seen = set(tickets)
    for number in range(len(tickets) + 1):
        if number not in seen:
            return number
    raise ValueError("nothing missing")


def missing_ticket_math(tickets: list[int]) -> int:
    """O(n) time, O(1) space: expected total (Gauss) minus actual total."""
    n = len(tickets)
    return n * (n + 1) // 2 - sum(tickets)


# ------------------------------------------------------------------ worked problem 2
# First animal name that appears exactly once in the zoo's visitor-favorite list.
def first_unique_brute(names: list[str]) -> str | None:
    """O(n^2): count each name by scanning the whole list."""
    for name in names:
        if names.count(name) == 1:
            return name
    return None


def first_unique_counting(names: list[str]) -> str | None:
    """O(n): one pass to count, one pass to find the first count of 1."""
    counts: dict[str, int] = {}
    for name in names:
        counts[name] = counts.get(name, 0) + 1
    for name in names:
        if counts[name] == 1:
            return name
    return None


# ------------------------------------------------------------------ worked problem 3
# Merge two sorted waiting lists (by arrival minute) into one sorted list.
def merge_brute(a: list[int], b: list[int]) -> list[int]:
    """O((a+b) log(a+b)): glue and sort - correct, but ignores that inputs are already sorted."""
    return sorted(a + b)


def merge_two_pointers(a: list[int], b: list[int]) -> list[int]:
    """O(a+b): repeatedly take the smaller front item - like merging two queues at a gate."""
    result: list[int] = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
            j += 1
    result.extend(a[i:])
    result.extend(b[j:])
    return result


# ------------------------------------------------------------------ industry problem 1
# Airport gates: can one gate handle all these flights without overlap?
def gate_conflict_brute(slots: list[tuple[int, int]]) -> bool:
    """O(n^2): compare every pair of (start, end) time slots."""
    for i in range(len(slots)):
        for j in range(i + 1, len(slots)):
            s1, e1 = slots[i]
            s2, e2 = slots[j]
            if s1 < e2 and s2 < e1:
                return True
    return False


def gate_conflict_sorted(slots: list[tuple[int, int]]) -> bool:
    """O(n log n): sort by start time; only NEIGHBORS can overlap first."""
    ordered = sorted(slots)
    for k in range(1, len(ordered)):
        if ordered[k][0] < ordered[k - 1][1]:
            return True
    return False


# ------------------------------------------------------------------ industry problem 2
# Bank: on which day does the balance first go below zero?
def first_negative_day(opening: int, daily_changes: list[int]) -> int:
    """O(n): a running total (accumulator) with early exit. Returns -1 if never negative."""
    balance = opening
    for day, change in enumerate(daily_changes, start=1):
        balance += change
        if balance < 0:
            return day
    return -1


# ------------------------------------------------------------------ industry problem 3
# Hospital: earliest free appointment slot at or after the time a patient asks for.
def earliest_slot(free_slots: list[int], requested: int) -> int | None:
    """O(log n) with a sorted list: lower-bound binary search (Chapter 11)."""
    low, high = 0, len(free_slots)
    while low < high:
        middle = (low + high) // 2
        if free_slots[middle] < requested:
            low = middle + 1
        else:
            high = middle
    return free_slots[low] if low < len(free_slots) else None


# ------------------------------------------------------------------ the stress tester
def stress_test(slow: Callable, fast: Callable, make_input: Callable[[random.Random], tuple],
                trials: int = 500, seed: int = 0) -> tuple | None:
    """Run both versions on many random inputs. Return the first input where they disagree."""
    rng = random.Random(seed)
    for _ in range(trials):
        args = make_input(rng)
        if slow(*args) != fast(*args):
            return args
    return None


def random_tickets(rng: random.Random) -> tuple[list[int]]:
    n = rng.randint(1, 30)
    tickets = list(range(n + 1))
    tickets.remove(rng.randint(0, n))
    rng.shuffle(tickets)
    return (tickets,)


def random_slots(rng: random.Random) -> tuple[list[tuple[int, int]]]:
    slots = []
    for _ in range(rng.randint(0, 8)):
        start = rng.randint(0, 100)
        slots.append((start, start + rng.randint(1, 20)))
    return (slots,)


if __name__ == "__main__":
    tickets = [3, 0, 1, 5, 4]
    print("Missing ticket:", missing_ticket_brute(tickets), missing_ticket_set(tickets), missing_ticket_math(tickets))
    favorites = ["lion", "otter", "lion", "panda", "otter", "zebra"]
    print("First unique favorite:", first_unique_counting(favorites))
    print("Merged waiting list:", merge_two_pointers([1, 4, 9], [2, 3, 10, 12]))
    print("Gate conflict?", gate_conflict_sorted([(900, 945), (1000, 1030), (940, 1000)]))
    print("First negative day:", first_negative_day(100, [-30, 20, -80, -40, 50]))
    print("Earliest slot at/after 10:20:", earliest_slot([900, 930, 1000, 1045, 1130], 1020))
    print("Stress test tickets:", stress_test(missing_ticket_brute, missing_ticket_math, random_tickets))
    print("Stress test gates:", stress_test(gate_conflict_brute, gate_conflict_sorted, random_slots))
