"""Volume 7, Chapter 7 - Thinking Problems (Section 7.17): model solutions.

Run:  python3 ch07_solutions.py
"""

from __future__ import annotations

import math


def bounded_choices(n: int, k: int, c: int) -> int:
    """Thinking Problem 2: ways to pick k items from n kinds with at most c of each kind.

    Stars and bars counts every choice; inclusion-exclusion removes those where some kind is used c + 1 or
    more times: put c + 1 of each of i chosen kinds aside, and spread the rest freely.
    """
    if n == 0:
        return 1 if k == 0 else 0
    total, i = 0, 0
    while i <= n and i * (c + 1) <= k:
        rest = k - i * (c + 1)
        total += (-1) ** i * math.comb(n, i) * math.comb(n + rest - 1, rest)
        i += 1
    return total


def at_least_one_overcount(novels: int, atlases: int, k: int) -> int:
    """Thinking Problem 3: the WRONG count 'pick one novel, then any k - 1 of the rest'."""
    return novels * math.comb(novels + atlases - 1, k - 1)


def odd_entries(n: int) -> int:
    """Thinking Problem 1: how many entries of row n of Pascal's triangle are odd (Lucas: 2^(1 bits of n))."""
    return sum(math.comb(n, k) % 2 for k in range(n + 1))


if __name__ == "__main__":
    print(bounded_choices(3, 4, 2), bounded_choices(3, 4, 4), at_least_one_overcount(5, 5, 3), math.comb(10, 3) - math.comb(5, 3))
    print([odd_entries(n) for n in range(9)])
