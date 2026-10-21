"""Volume 5, Chapter 1 - Remembering Answers: memoization turns repeated work into look-ups.

Run:  python3 ch01_examples.py
"""

from __future__ import annotations

from collections import Counter


def ways(n: int, steps=(1, 2), calls: Counter | None = None) -> int:
    """Ways to climb n stairs taking any of the given step sizes, by plain recursion (Figure 1.2)."""
    if calls is not None:
        calls[n] += 1
    if n < 0:
        return 0
    if n == 0:
        return 1
    return sum(ways(n - s, steps, calls) for s in steps)


def ways_memo(n: int, steps=(1, 2), memo: dict | None = None, solved: list | None = None) -> int:
    """The same recursion, remembering each answer the first time it is found (Figure 1.3)."""
    if memo is None:
        memo = {}
    if n < 0:
        return 0
    if n == 0:
        return 1
    if n not in memo:
        if solved is not None:
            solved[0] += 1
        memo[n] = sum(ways_memo(n - s, steps, memo, solved) for s in steps)
    return memo[n]


if __name__ == "__main__":
    c = Counter()
    print(ways(6, calls=c), sum(c.values()), sorted(c.items()))
    for n in (10, 20, 30):
        c, s = Counter(), [0]
        print(n, ways(n, calls=c), sum(c.values()), ways_memo(n, solved=s), s[0])
    print(ways(10, (1, 2, 3)), ways_memo(50), ways_memo(10, (2,)), ways_memo(9, (2,)), ways(0), ways_memo(0))
