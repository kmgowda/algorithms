"""Volume 1, Chapter 7, Thinking Problem 2 - the largest input that fits a step budget, found with about
2 log2 n evaluations of the step formula (doubling, then halving).

Run:  python3 ch07_solutions.py
"""

from __future__ import annotations

import math
from typing import Callable


def largest_fitting(f: Callable[[int], float], budget: float) -> tuple[int, int]:
    """Largest n with f(n) <= budget, for a step formula f that grows with n and has f(1) <= budget.
    Returns (n, evaluations of f). Doubling finds a size that does not fit; halving the gap finds the edge."""
    evaluations = 0
    lo = 1
    while True:
        evaluations += 1
        if f(2 * lo) > budget:
            break
        lo = 2 * lo
    hi = 2 * lo - 1                       # f(lo) fits and f(hi + 1) = f(2 lo) does not
    while lo < hi:
        mid = (lo + hi + 1) // 2
        evaluations += 1
        if f(mid) <= budget:
            lo = mid
        else:
            hi = mid - 1
    return lo, evaluations


if __name__ == "__main__":
    print(largest_fitting(lambda n: n * math.log2(n), 1e7))
    print(largest_fitting(lambda n: 2 ** n, 1e7))
