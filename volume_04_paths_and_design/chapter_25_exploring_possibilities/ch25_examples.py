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


def search(state, candidates, is_solution, process, log: list | None = None) -> None:
    """Skiena's general form (Section 25.4): a partial answer is a state; extend it by each candidate in turn.
    candidates(state) -> list; is_solution(state) -> bool; process(state) records a finished answer."""
    if log is not None:
        log.append(list(state))
    if is_solution(state):
        process(list(state))
        return
    for c in candidates(state):
        state.append(c)
        search(state, candidates, is_solution, process, log)
        state.pop()


def seatings_by_search(readers: list, check_early: bool = False) -> tuple[list, int]:
    """The seating problem written in Skiena's form. check_early=True offers only readers who do not sit an
    Ana-Ben pair side by side, so dead branches are never entered. Returns (valid seatings, nodes)."""
    out, log = [], []

    def candidates(row):
        left = [r for r in readers if r not in row]
        if check_early and row:
            left = [r for r in left if {row[-1], r} != {"Ana", "Ben"}]
        return left

    def is_solution(row):
        return len(row) == len(readers)

    def process(row):
        if allowed(row):
            out.append(row)

    search([], candidates, is_solution, process, log)
    return out, len(log)


def merge_sort_calls(values: list, log: list | None = None) -> list:
    """Merge sort that records every call (Figure 25.4, left): every call is needed for the one answer."""
    if log is not None:
        log.append(list(values))
    if len(values) <= 1:
        return list(values)
    mid = len(values) // 2
    a, b = merge_sort_calls(values[:mid], log), merge_sort_calls(values[mid:], log)
    out = []
    while a and b:
        out.append(a.pop(0) if a[0] <= b[0] else b.pop(0))
    return out + a + b


if __name__ == "__main__":
    s = all_seatings(READERS)
    good = [r for r in s if allowed(r)]
    log = []
    found = explore(READERS, None, log)
    print(len(s), len(good), len(found), len(log), tree_size(4))
    print(good[:3])
    print([tree_size(n) for n in (1, 2, 3, 4, 5, 8, 10)])
