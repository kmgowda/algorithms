"""Volume 6, Chapter 9 - Remembering Answers: memoization turns repeated work into look-ups.

Run:  python3 ch09_examples.py
"""

from __future__ import annotations

from collections import Counter


def ways(n: int, steps=(1, 2), calls: Counter | None = None) -> int:
    """Ways to climb n stairs taking any of the given step sizes, by plain recursion (Figure 9.2)."""
    if calls is not None:
        calls[n] += 1
    if n < 0:
        return 0
    if n == 0:
        return 1
    return sum(ways(n - s, steps, calls) for s in steps)


def ways_memo(n: int, steps=(1, 2), memo: dict | None = None, solved: list | None = None) -> int:
    """The same recursion, remembering each answer the first time it is found (Figure 9.4)."""
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


def plain_calls(n: int, steps=(1, 2)) -> int:
    """How many calls plain recursion makes for n stairs, without making them: the calls obey their own
    recurrence, calls(n) = 1 + sum of calls(n - s), with calls(n) = 1 when n <= 0 (Section 9.4)."""
    table = {}
    for m in range(min(0, n) - max(steps, default=0), n + 1):
        table[m] = 1 if m <= 0 else 1 + sum(table[m - s] for s in steps)
    return table[n]


def ways_avoiding(n: int, blocked=(), steps=(1, 2), memo: dict | None = None) -> int:
    """Ways to climb n stairs without standing on any blocked step (Practice Problem 3)."""
    memo = {} if memo is None else memo
    if n < 0 or n in blocked:
        return 0
    if n == 0:
        return 1
    if n not in memo:
        memo[n] = sum(ways_avoiding(n - s, blocked, steps, memo) for s in steps)
    return memo[n]


def memo_trace(n: int, steps=(1, 2)) -> list:
    """The order in which the remembering version first solves each sub-problem, and its look-ups
    (Figure 9.5): a list of ("solve", m) and ("look up", m) events."""
    memo, events = {}, []

    def go(m: int) -> int:
        if m < 0:
            return 0
        if m == 0:
            return 1
        if m in memo:
            events.append(("look up", m))
            return memo[m]
        events.append(("solve", m))
        memo[m] = sum(go(m - s) for s in steps)
        return memo[m]

    go(n)
    return events


if __name__ == "__main__":
    c = Counter()
    print(ways(6, calls=c), sum(c.values()), sorted(c.items()))
    for n in (10, 20, 30):
        c, s = Counter(), [0]
        print(n, ways(n, calls=c), sum(c.values()), ways_memo(n, solved=s), s[0])
    print(ways(10, (1, 2, 3)), ways_memo(50), ways_memo(10, (2,)), ways_memo(9, (2,)), ways(0), ways_memo(0))
