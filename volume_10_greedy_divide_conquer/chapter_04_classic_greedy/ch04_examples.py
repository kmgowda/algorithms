"""Volume 10, Chapter 4 - Classic Greedy: Activity Selection, Interval Scheduling, Coin Change,
Fractional Knapsack, Job Sequencing.

Run:  python3 ch04_examples.py
"""

from __future__ import annotations

import heapq


def activity_selection(events: list[tuple[str, int, int]]) -> list[str]:
    """Most non-overlapping events in one hall: earliest finish first (proved in Chapter 3)."""
    chosen, last_end = [], float("-inf")
    for name, start, end in sorted(events, key=lambda e: e[2]):
        if start >= last_end:
            chosen.append(name)
            last_end = end
    return chosen


def rooms_needed(meetings: list[tuple[int, int]]) -> int:
    """Interval partitioning: fewest rooms so no two overlapping meetings share one.
    Greedy by start time; reuse the room that frees up earliest (a min-heap of end times). Equals the max overlap."""
    ends: list[int] = []
    for start, end in sorted(meetings):
        if ends and ends[0] <= start:
            heapq.heapreplace(ends, end)
        else:
            heapq.heappush(ends, end)
    return len(ends)


def fractional_knapsack(items: list[tuple[str, float, float]], capacity: float) -> tuple[float, dict[str, float]]:
    """items = (name, weight, value); you may take PART of an item (spices, grain).
    Greedy: best value per kilogram first. Returns (total value, kilograms taken of each)."""
    taken: dict[str, float] = {}
    total = 0.0
    for name, weight, value in sorted(items, key=lambda it: it[2] / it[1], reverse=True):
        if capacity <= 0:
            break
        amount = min(weight, capacity)
        taken[name] = amount
        total += value * amount / weight
        capacity -= amount
    return total, taken


def job_sequencing(jobs: list[tuple[str, int, int]]) -> tuple[int, list[str]]:
    """Each job takes one day, has a deadline (day number) and a profit; one job per day.
    Greedy: most profitable first, placed in the LATEST free day before its deadline. Returns (profit, schedule)."""
    last_day = max((d for _, d, _ in jobs), default=0)
    slot: list[str | None] = [None] * (last_day + 1)
    profit = 0
    for name, deadline, gain in sorted(jobs, key=lambda j: -j[2]):
        for day in range(min(deadline, last_day), 0, -1):
            if slot[day] is None:
                slot[day], profit = name, profit + gain
                break
    return profit, [s for s in slot[1:] if s is not None]


def is_canonical(coins: list[int], limit: int | None = None) -> bool:
    """Practical check: does largest-coin-first give the fewest coins for every amount up to a limit?
    (Compared with dynamic programming; for real currencies the answer is yes.)"""
    coins = sorted(coins)
    limit = limit or coins[-1] * 2
    best = [0] + [10 ** 9] * limit
    for a in range(1, limit + 1):
        best[a] = min((best[a - c] + 1 for c in coins if c <= a), default=10 ** 9)
    for a in range(1, limit + 1):
        rest, count = a, 0
        for c in reversed(coins):
            count += rest // c
            rest %= c
        if rest == 0 and count != best[a]:
            return False
    return True


if __name__ == "__main__":
    events = [("yoga", 1, 4), ("chess", 3, 5), ("film", 0, 6), ("quiz", 5, 7), ("music", 3, 9),
              ("art", 5, 9), ("drama", 6, 10), ("dance", 8, 11)]
    print("hall bookings:", activity_selection(events))
    print("rooms:", rooms_needed([(9, 10), (9, 12), (11, 13), (13, 14)]))
    print("spice knapsack:", fractional_knapsack([("saffron", 1, 60), ("pepper", 3, 90), ("cumin", 2, 30)], 3))
    print("job sequencing:", job_sequencing([("a", 2, 100), ("b", 1, 19), ("c", 2, 27), ("d", 1, 25), ("e", 3, 15)]))
    print("canonical:", is_canonical([1, 2, 5, 10, 20, 50]), is_canonical([1, 3, 4]))
