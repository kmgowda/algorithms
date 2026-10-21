"""Volume 4, Chapter 25 - Exploring Every Possibility: the tree of choices, and why it grows so fast.

Run:  python3 ch25_examples.py
"""

from __future__ import annotations

import itertools

# Seat four readers in a row; Ana and Ben must not sit side by side.
READERS = ["Ana", "Ben", "Cai", "Dev"]


def all_seatings(readers: list) -> list:
    return [list(p) for p in itertools.permutations(readers)]


def allowed(row: list) -> bool:
    return all({a, b} != {"Ana", "Ben"} for a, b in zip(row, row[1:]))


def explore(readers: list, row: list | None = None, log: list | None = None) -> list:
    """Build a seating one seat at a time, trying every reader left for the next seat (Figure 25.2)."""
    row = row or []
    if log is not None:
        log.append(list(row))
    if len(row) == len(readers):
        return [list(row)] if allowed(row) else []
    found = []
    for r in readers:
        if r not in row:
            found += explore(readers, row + [r], log)
    return found


def tree_size(n: int) -> int:
    """Nodes in the full tree of seatings: 1 + n + n(n-1) + ... + n!."""
    total, level = 1, 1
    for k in range(n, 0, -1):
        level *= k
        total += level
    return total


if __name__ == "__main__":
    s = all_seatings(READERS)
    good = [r for r in s if allowed(r)]
    log = []
    found = explore(READERS, None, log)
    print(len(s), len(good), len(found), len(log), tree_size(4))
    print(good[:3])
    print([tree_size(n) for n in (1, 2, 3, 4, 5, 8, 10)])
