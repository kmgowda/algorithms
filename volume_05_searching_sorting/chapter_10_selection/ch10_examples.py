"""Volume 5, Chapter 10 - Selection Problems: k-th Smallest, Quickselect, Median of Medians.

Run:  python3 ch10_examples.py
"""

from __future__ import annotations

import heapq
import random


def kth_smallest_by_sorting(values: list, k: int):
    """The simple way: sort, then index. O(n log n). k counts from 1."""
    return sorted(values)[k - 1]


def quickselect(values: list, k: int, rng: random.Random | None = None):
    """Hoare's quickselect: partition like quicksort, but continue into ONE side only. Expected O(n)."""
    if not 1 <= k <= len(values):
        raise ValueError("k out of range")
    rng = rng or random
    items = list(values)
    target = k - 1
    while True:
        pivot = rng.choice(items)
        smaller = [x for x in items if x < pivot]
        equal = [x for x in items if x == pivot]
        if target < len(smaller):
            items = smaller
        elif target < len(smaller) + len(equal):
            return pivot
        else:
            target -= len(smaller) + len(equal)
            items = [x for x in items if x > pivot]


def median_of_medians(values: list, k: int):
    """Deterministic selection (Blum, Floyd, Pratt, Rivest, Tarjan): a pivot guaranteed to be 'good enough',
    so the worst case is O(n) too. Groups of 5 -> medians -> recursive median of those medians."""
    if len(values) <= 5:
        return sorted(values)[k - 1]
    medians = [sorted(values[i:i + 5])[len(values[i:i + 5]) // 2] for i in range(0, len(values), 5)]
    pivot = median_of_medians(medians, (len(medians) + 1) // 2)
    smaller = [x for x in values if x < pivot]
    equal = [x for x in values if x == pivot]
    if k <= len(smaller):
        return median_of_medians(smaller, k)
    if k <= len(smaller) + len(equal):
        return pivot
    return median_of_medians([x for x in values if x > pivot], k - len(smaller) - len(equal))


def median(values: list[float]) -> float:
    """Median in expected O(n) using quickselect (average of the two middles for even counts)."""
    n = len(values)
    if n == 0:
        raise ValueError("median of empty list")
    if n % 2:
        return quickselect(values, n // 2 + 1)
    return (quickselect(values, n // 2) + quickselect(values, n // 2 + 1)) / 2


def p95_latency(latencies_ms: list[float]) -> float:
    """Industry example: the 95th-percentile response time (V2-C12) without sorting all requests."""
    k = max(1, -(-95 * len(latencies_ms) // 100))       # ceiling of 0.95 * n (nearest-rank)
    return quickselect(latencies_ms, k)


def closest_shops(shops: list[tuple[str, float, float]], k: int) -> list[str]:
    """Industry example (LeetCode 973 idea): the k shops nearest to the user at (0, 0) - a size-k heap."""
    nearest = heapq.nsmallest(k, shops, key=lambda s: s[1] ** 2 + s[2] ** 2)
    return [name for name, _, _ in nearest]


if __name__ == "__main__":
    heights = [152, 167, 141, 180, 158, 173, 149]
    print(kth_smallest_by_sorting(heights, 3), quickselect(heights, 3, random.Random(1)), median_of_medians(heights, 3))
    print("median height:", median(heights))
    rng = random.Random(2)
    times = [rng.uniform(20, 60) for _ in range(990)] + [rng.uniform(300, 900) for _ in range(10)]
    print("p95 latency:", round(p95_latency(times), 1))
    print(closest_shops([("Bakery", 3, 4), ("Pharmacy", 1, 1), ("Bookshop", -2, 2), ("Florist", 6, 1)], 2))
