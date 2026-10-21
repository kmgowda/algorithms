"""Volume 6, Chapter 30 - The Road Ahead: Choosing an Algorithm (the series in one decision guide).

Run:  python3 ch30_examples.py
"""

from __future__ import annotations

import math

GROWTH = {"n": lambda n: n, "n log n": lambda n: n * math.log2(max(n, 2)), "n^2": lambda n: n ** 2, "n^3": lambda n: n ** 3,
          "2^n": lambda n: 2 ** n, "n!": lambda n: math.factorial(n)}


def largest_input(rate: str, budget: int) -> int:
    """The largest n whose cost fits the budget of steps (Figure 30.1), by doubling then binary search."""
    f = GROWTH[rate]
    if f(1) > budget:
        return 0
    hi = 1
    while f(hi * 2) <= budget:
        hi *= 2
    lo, hi = hi, hi * 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        lo, hi = (mid, hi) if f(mid) <= budget else (lo, mid)
    return lo


RULES = [  # (question, answer, where in the series)
    ("data changes and you search it often", "a hash table or balanced tree", "Volume 2"),
    ("you need the order of the data", "sort it", "Volume 3, Part II"),
    ("routes on a map with weights", "Dijkstra, or Bellman-Ford with negative roads", "Volume 4, Part I"),
    ("best choice looks safe at each step and you can prove it", "greedy", "Volume 4, Part II"),
    ("sub-problems repeat", "dynamic programming", "Volume 5, Part I"),
    ("searching text", "KMP, Horspool, Aho-Corasick, or a suffix array", "Volume 5, Part II"),
    ("the problem is NP-hard", "approximate, search locally, or solve small cases exactly", "Volume 6, Part V"),
    ("the data is too big to store", "stream with sketches, or spread it with MapReduce", "Volume 6, Part VI"),
]


def advise(situation: str) -> list:
    words = set(situation.lower().split())
    return [(a, where) for q, a, where in RULES if words & set(q.split()) - {"the", "a", "and", "you", "it", "is", "to", "of", "with", "on", "at", "each"}]


if __name__ == "__main__":
    for rate in GROWTH:
        print(rate, largest_input(rate, 10 ** 8))
    print(advise("sub-problems repeat"), advise("too big to store"))
