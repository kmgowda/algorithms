"""Volume 4, Chapter 5 - Thinking Problems (Section 5.15): model solutions.

Run:  python3 ch05_solutions.py
"""

from __future__ import annotations

PILE = [58, 25, 91, 12, 70, 47, 84, 31, 63]


def cycle_count(a: list) -> int:
    """Thinking Problem 1: the cycles of 'where does the book at this position belong'."""
    order = sorted(range(len(a)), key=lambda i: a[i])
    target = [0] * len(a)
    for r, i in enumerate(order):
        target[i] = r
    seen, cycles = [False] * len(a), 0
    for i in range(len(a)):
        if not seen[i]:
            cycles += 1
            while not seen[i]:
                seen[i] = True
                i = target[i]
    return cycles


def crate_swap_plan(a: list) -> list[tuple[int, int]]:
    """Thinking Problem 2: a list of swaps that sorts a, n - cycles of them, found in O(n log n)."""
    order = sorted(range(len(a)), key=lambda i: a[i])
    target = [0] * len(a)
    for r, i in enumerate(order):
        target[i] = r
    plan = []
    for i in range(len(a)):
        while target[i] != i:
            t = target[i]
            plan.append((i, t))
            target[i], target[t] = target[t], target[i]
    return plan


def double_selection_sort(a: list) -> None:
    """Thinking Problem 3, corrected: place the smallest at the front and the largest at the back."""
    lo, hi = 0, len(a) - 1
    while lo < hi:
        small = large = lo
        for k in range(lo + 1, hi + 1):
            if a[k] < a[small]:
                small = k
            if a[k] > a[large]:
                large = k
        a[lo], a[small] = a[small], a[lo]
        if large == lo:                      # the first swap moved the largest book
            large = small
        a[hi], a[large] = a[large], a[hi]
        lo, hi = lo + 1, hi - 1


def apply_plan(a: list, plan: list[tuple[int, int]]) -> list:
    b = list(a)
    for i, j in plan:
        b[i], b[j] = b[j], b[i]
    return b


if __name__ == "__main__":
    print(cycle_count(PILE), crate_swap_plan(PILE))
    b = list(PILE)
    double_selection_sort(b)
    print(b)
