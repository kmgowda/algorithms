"""Volume 6, Chapter 29 - Parallel Algorithms: work, span, and how many helpers really help.

Run:  python3 ch29_examples.py
"""

from __future__ import annotations

import math


def tree_sum(values: list) -> tuple[int, int, int]:
    """Add pairs in rounds, all pairs of a round at once (Figure 29.1). Returns (total, additions = work, rounds = span)."""
    level, work, rounds = list(values), 0, 0
    if not level:
        return 0, 0, 0
    while len(level) > 1:
        nxt = [level[i] + level[i + 1] for i in range(0, len(level) - 1, 2)]
        work += len(nxt)
        if len(level) % 2:
            nxt.append(level[-1])
        level, rounds = nxt, rounds + 1
    return level[0], work, rounds


def prefix_sums_parallel(values: list) -> tuple[list, int, int]:
    """Hillis-Steele scan (Figure 29.2): in round r, every position adds the value 2^r places to its left.
    Returns (running totals, additions, rounds)."""
    a, work, rounds, step = list(values), 0, 0, 1
    while step < len(a):
        a = [a[i] + (a[i - step] if i >= step else 0) for i in range(len(a))]
        work += len(a) - step
        rounds += 1
        step *= 2
    return a, work, rounds


def time_with_helpers(work: int, span: int, helpers: int) -> float:
    """Brent's bound: about work / helpers + span steps."""
    return work / helpers + span


def amdahl(parallel_share: float, helpers: int) -> float:
    """Speed-up when only part of a job can be shared out (Figure 29.3)."""
    return 1 / ((1 - parallel_share) + parallel_share / helpers)


if __name__ == "__main__":
    print(tree_sum(list(range(1, 17))), tree_sum(list(range(1, 1025)))[1:])
    print(prefix_sums_parallel([3, 1, 4, 1, 5, 9, 2, 6]))
    w, s = 1023, 10
    print([round(time_with_helpers(w, s, p), 1) for p in (1, 4, 32, 1024)])
    print([round(amdahl(0.9, p), 2) for p in (2, 8, 64, 1000)])
