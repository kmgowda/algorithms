"""Volume 2, Chapter 3 - Sets and Maps in Practice.

Run:  python3 ch03_examples.py
"""

from __future__ import annotations

import random

POETRY = {"Ana", "Ben", "Cai", "Dev"}
SCIENCE = {"Cai", "Dev", "Eva", "Fay", "Gus"}


def count_loans(loans: list[str]) -> dict[str, int]:
    """How many times each title appears, in one pass (Figure 3.2)."""
    counts: dict[str, int] = {}
    for title in loans:
        counts[title] = counts.get(title, 0) + 1
    return counts


def group_by(items, key) -> dict:
    """A map from key(item) to the list of items with that key (Figure 3.3)."""
    groups: dict = {}
    for it in items:
        groups.setdefault(key(it), []).append(it)
    return groups


def intersection(a: set, b: set) -> set:
    """Walk the smaller set and test each member against the larger (Section 3.4)."""
    small, large = (a, b) if len(a) <= len(b) else (b, a)
    return {x for x in small if x in large}


def reminders_fast(overdue: list[tuple[str, str]], opted_out: list[str]) -> dict[str, list[str]]:
    """Section 3.8: one entry per reader with their overdue titles, skipping opted-out readers."""
    skip = set(opted_out)
    out: dict[str, list[str]] = {}
    for reader, title in overdue:
        if reader not in skip:
            out.setdefault(reader, []).append(title)
    return out


def reminders_slow(overdue, opted_out):
    """The plain-list version: every loan is checked against the whole opt-out list."""
    out = {}
    for reader, title in overdue:
        if not any(reader == o for o in opted_out):
            out.setdefault(reader, []).append(title)
    return out


if __name__ == "__main__":
    print(sorted(POETRY | SCIENCE), sorted(intersection(POETRY, SCIENCE)), sorted(POETRY - SCIENCE),
          sorted(POETRY ^ SCIENCE))
    print(count_loans(["Maps", "Ocean", "Maps", "Clocks", "Maps", "Ocean"]), count_loans(list("BANANA")))
    print(group_by(["map", "mat", "ant", "apt", "man"], key=lambda w: w[0]))
    rng = random.Random(1)
    overdue = [(f"r{rng.randint(1, 3000)}", f"t{rng.randint(1, 500)}") for _ in range(2000)]
    opted = [f"r{rng.randint(1, 3000)}" for _ in range(500)]
    print(reminders_fast(overdue, opted) == reminders_slow(overdue, opted))
