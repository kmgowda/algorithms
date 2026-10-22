"""Volume 7, Chapter 19 - Thinking Problem 2: when the length n is known, take a fair sample of k in one pass,
in stream order, with no replacements (Knuth's selection sampling, Algorithm S).

Run:  python3 ch19_solutions.py
"""

from __future__ import annotations

import random


def selection_sample(stream, n: int, k: int, rng) -> list:
    """Take each item with chance (places still open) / (items still to come). Every k-subset is equally likely."""
    if not 0 <= k <= n:
        raise ValueError("need 0 <= k <= n")
    taken = []
    for seen, item in enumerate(stream):
        if len(taken) == k:
            break
        if rng.randrange(n - seen) < k - len(taken):
            taken.append(item)
    return taken


if __name__ == "__main__":
    print(selection_sample(range(1000), 1000, 3, random.Random(19)))
