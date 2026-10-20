"""Volume 1, Chapter 6 - Why Measure? Counting Steps.

Run:  python3 ch06_examples.py
"""

from __future__ import annotations

import timeit


def search_comparisons(shelf: list[int], target: int) -> int:
    """Comparisons made by linear search (the cost model of Figure 6.2)."""
    count = 0
    for book in shelf:
        count += 1
        if book == target:
            break
    return count


def pair_comparisons(n: int) -> int:
    """Comparisons made by checking every pair of n items once: n(n - 1) / 2."""
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            count += 1
    return count


def doubling_ratios(counts: list[int]) -> list[float]:
    """Each count divided by the previous one: about 2 for linear growth, 4 for quadratic (Figure 6.4)."""
    return [round(b / a, 2) for a, b in zip(counts, counts[1:])]


def repeated_timings(n: int, repeats: int = 12) -> list[float]:
    """Time the same failed search repeatedly (microseconds); the spread is noise (Figure 6.1)."""
    data = list(range(n))
    return [timeit.timeit(lambda: -1 in data, number=20) / 20 * 1e6 for _ in range(repeats)]


if __name__ == "__main__":
    print(search_comparisons([12, 25, 31, 47, 58, 63, 70, 84, 91], 63))
    sizes = [1000, 2000, 4000, 8000]
    print([n * (n - 1) // 2 for n in sizes], doubling_ratios([n * (n - 1) // 2 for n in sizes]))
    print([round(t) for t in repeated_timings(100_000)])
