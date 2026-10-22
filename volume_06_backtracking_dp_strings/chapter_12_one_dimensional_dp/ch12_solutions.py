"""Volume 6, Chapter 12 - Thinking Problems.

Problem 1: best[i] = max(best[i - 1], best[i - 2] + talks[i]) gives the best non-adjacent choice (checked by brute force).
Problem 2: evenings round a circle (the first and last are neighbours): solve two straight lines.
Problem 3: "take the biggest evening, drop its neighbours, repeat" can lose; a smallest counterexample.
"""

from __future__ import annotations

import itertools

from ch12_examples import best_evenings


def brute_evenings(talks: list) -> int:
    n, best = len(talks), 0
    for mask in range(1 << n):
        if mask & (mask >> 1) == 0:
            best = max(best, sum(talks[i] for i in range(n) if mask >> i & 1))
    return best


def best_circle(talks: list) -> int:
    if len(talks) <= 1:
        return sum(talks)
    return max(best_evenings(talks[:-1])[0], best_evenings(talks[1:])[0])


def brute_circle(talks: list) -> int:
    n, best = len(talks), 0
    for mask in range(1 << n):
        ok = mask & (mask >> 1) == 0 and not (n > 1 and mask & 1 and mask >> (n - 1) & 1)
        if ok:
            best = max(best, sum(talks[i] for i in range(n) if mask >> i & 1))
    return best


def greedy_biggest(talks: list) -> int:
    left, total = set(range(len(talks))), 0
    while left:
        i = max(left, key=lambda j: (talks[j], -j))
        total += talks[i]
        left -= {i - 1, i, i + 1}
    return total


def greedy_trap() -> list:
    for n in range(1, 6):
        for t in itertools.product(range(1, 6), repeat=n):
            if greedy_biggest(list(t)) < brute_evenings(list(t)):
                return list(t)
    return None


if __name__ == "__main__":
    from ch12_examples import TALKS
    print(best_evenings(TALKS)[0], best_circle(TALKS), greedy_trap(), greedy_biggest(TALKS))
