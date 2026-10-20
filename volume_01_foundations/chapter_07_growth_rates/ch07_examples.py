"""Volume 1, Chapter 7 - Growth Rates.

Run:  python3 ch07_examples.py
"""

from __future__ import annotations

import math


def steps(rate: str, n: int) -> float:
    """Steps taken by each common growth rate for input size n (n >= 1), as in the table of Section 7.4."""
    formulas = {"1": lambda: 1, "log n": lambda: math.log2(n), "n": lambda: n,
                "n log n": lambda: n * math.log2(n), "n^2": lambda: n * n, "n^3": lambda: n ** 3,
                "2^n": lambda: 2 ** n}
    return formulas[rate]()


def largest_n(rate: str, budget: float = 1e7) -> int:
    """The largest n whose step count fits in `budget` steps (Figure 7.6): double n until it no longer fits,
    then binary-search between the last size that fitted and the first that did not."""
    hi = 1
    while steps(rate, hi * 2) <= budget:
        hi *= 2
    lo, hi = hi, hi * 2
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if steps(rate, mid) <= budget:
            lo = mid
        else:
            hi = mid - 1
    return lo


def halvings(n: int) -> int:
    """How many halvings reduce n items to one (Figure 7.5)."""
    count = 0
    while n > 1:
        n //= 2
        count += 1
    return count


def grains_on_square(k: int) -> int:
    """Rice grains on square k of the chessboard (Figure 7.1): 2^(k-1)."""
    return 2 ** (k - 1)


if __name__ == "__main__":
    for r in ("n", "n log n", "n^2", "n^3", "2^n"):
        print(r, largest_n(r))
    print(halvings(16), halvings(1_000_000), grains_on_square(11), sum(grains_on_square(k) for k in range(1, 11)))
