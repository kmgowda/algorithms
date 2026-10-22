"""Volume 1, Chapter 15, Thinking Problem 2 - every subset, each one item different from the last.

Maya changes the prize display one book at a time: put one book in, or take one out. The order
(a reflected Gray code) lists the subsets of the rest, then the same list backwards with the first item added,
so the join between the two halves changes only the first item.

Run:  python3 ch15_solutions.py
"""

from __future__ import annotations


def gray_order(items: list[str]) -> list[list[str]]:
    """Every subset of items, each differing from the one before by exactly one item."""
    if not items:
        return [[]]
    order = gray_order(items[1:])
    return order + [[items[0]] + g for g in reversed(order)]


def changed_items(order: list[list[str]]) -> list[str]:
    """The item put in or taken out at each step of an order of subsets (exactly one per step)."""
    steps = []
    for before, after in zip(order, order[1:]):
        diff = set(before) ^ set(after)
        if len(diff) != 1:
            raise ValueError("two neighbouring subsets differ in more than one item")
        steps.append(diff.pop())
    return steps


def distinct_permutations(items: list[str]) -> list[list[str]]:
    """Every different arrangement of items that may repeat: each value is tried only once as the first item
    (the fix of Thinking Problem 3)."""
    if not items:
        return [[]]
    result, tried = [], set()
    for i, x in enumerate(items):
        if x in tried:
            continue
        tried.add(x)
        for p in distinct_permutations(items[:i] + items[i + 1:]):
            result.append([x] + p)
    return result


if __name__ == "__main__":
    order = gray_order(list("ABC"))
    print(["".join(s) or "{}" for s in order], changed_items(order))
    print(["".join(p) for p in distinct_permutations(list("ABA"))])
