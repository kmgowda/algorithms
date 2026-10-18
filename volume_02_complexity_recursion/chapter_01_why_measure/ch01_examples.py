"""Volume 2, Chapter 1 - Why Measure? Experiments vs. Counting Steps.

Run:  python3 ch01_examples.py
"""

from __future__ import annotations

import math
import time
import timeit
from typing import Callable


# ------------------------------------------------------------------ things to measure
def find_book_linear(shelf: list[int], wanted: int) -> int:
    """Linear search over a shelf of book IDs. Returns the index or -1."""
    for index, book in enumerate(shelf):
        if book == wanted:
            return index
    return -1


def count_matching_pairs(tags: list[int]) -> int:
    """Quadratic work: how many pairs of visitors wear the same badge color?"""
    pairs = 0
    for i in range(len(tags)):
        for j in range(i + 1, len(tags)):
            if tags[i] == tags[j]:
                pairs += 1
    return pairs


# ------------------------------------------------------------------ counting steps instead of seconds
def linear_steps(n: int) -> int:
    """Comparisons made by a worst-case linear search on n items (target missing)."""
    steps = 0
    for _ in range(n):
        steps += 1
    return steps


def pair_steps(n: int) -> int:
    """Comparisons made by comparing every pair of n items."""
    steps = 0
    for i in range(n):
        for _ in range(i + 1, n):
            steps += 1
    return steps


def halving_steps(n: int) -> int:
    """Steps made by a loop that halves n until it reaches 1."""
    steps = 0
    while n > 1:
        n //= 2
        steps += 1
    return steps


# ------------------------------------------------------------------ timing
def best_time(function: Callable[[], object], repeats: int = 5) -> float:
    """Seconds for the fastest of several runs. The minimum is the least disturbed by noise."""
    best = float("inf")
    for _ in range(repeats):
        start = time.perf_counter()
        function()
        best = min(best, time.perf_counter() - start)
    return best


def timeit_seconds(statement: Callable[[], object], number: int = 100, repeat: int = 5) -> float:
    """Average seconds per call using the standard library's timeit (best of `repeat` batches)."""
    batches = timeit.repeat(statement, number=number, repeat=repeat)
    return min(batches) / number


# ------------------------------------------------------------------ the doubling experiment
def doubling_ratios(cost: Callable[[int], float], sizes: list[int]) -> list[float]:
    """For each size after the first: cost(n) / cost(previous n).

    If each size is double the previous one, a ratio near 2 suggests O(n),
    near 4 suggests O(n^2), near 8 suggests O(n^3), and near 1 suggests O(1) or O(log n).
    """
    costs = [cost(n) for n in sizes]
    return [costs[k] / costs[k - 1] for k in range(1, len(costs))]


def estimated_exponent(ratio: float) -> float:
    """If cost grows like n^b, doubling n multiplies cost by 2^b, so b = log2(ratio)."""
    return math.log2(ratio)


def timed_cost(function: Callable[[list[int]], object]) -> Callable[[int], float]:
    """Turn 'function on a list of n items' into 'seconds for size n', for doubling experiments."""
    def cost(n: int) -> float:
        data = list(range(n))
        return best_time(lambda: function(data), repeats=3)
    return cost


if __name__ == "__main__":
    shelf = list(range(200_000))
    print(f"Linear search, worst case: {best_time(lambda: find_book_linear(shelf, -1)):.5f} s")
    print(f"Same with timeit:          {timeit_seconds(lambda: find_book_linear(shelf, -1), number=5):.5f} s")

    sizes = [1000, 2000, 4000, 8000]
    for name, cost in (("linear", linear_steps), ("pairs", pair_steps), ("halving", halving_steps)):
        ratios = doubling_ratios(cost, sizes)
        print(f"{name:8} step ratios: {[round(r, 2) for r in ratios]}")

    timed = doubling_ratios(timed_cost(lambda data: find_book_linear(data, -1)), [50_000, 100_000, 200_000])
    print("timed linear ratios:", [round(r, 2) for r in timed])
    timed = doubling_ratios(timed_cost(count_matching_pairs), [300, 600, 1200])
    print("timed pairs ratios: ", [round(r, 2) for r in timed],
          "-> exponent about", round(estimated_exponent(timed[-1]), 1))
