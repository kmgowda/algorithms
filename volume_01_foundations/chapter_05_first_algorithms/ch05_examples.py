"""Volume 1, Chapter 5 - First Algorithms: Totals, Maximums, and Linear Search.

Run:  python3 ch05_examples.py
"""

from __future__ import annotations

SHELF = [12, 25, 31, 47, 58, 63, 70, 84, 91]
VISITS = [("Mon", 34), ("Tue", 41), ("Wed", 29), ("Thu", 56), ("Fri", 48), ("Sat", 61), ("Sun", 22)]


def running_totals(values: list[int]) -> list[int]:
    """The running total after each item (Figure 5.1)."""
    total, out = 0, []
    for v in values:
        total = total + v
        out.append(total)
    return out


def max_with_position(values: list[int]) -> tuple[int, int]:
    """Largest value and the position where it first appears; values must not be empty (Figure 5.2)."""
    best, where = values[0], 0
    for i in range(1, len(values)):
        if values[i] > best:
            best, where = values[i], i
    return best, where


def linear_search(shelf: list[int], target: int) -> int:
    """Position of the first item equal to target, or -1 if it is absent (Figures 5.4 and 5.5)."""
    for i in range(len(shelf)):
        if shelf[i] == target:
            return i
    return -1


def linear_search_sentinel(shelf: list[int], target: int) -> int:
    """Linear search with a sentinel (Section 5.6): a copy of the target is put after the last item, so the
    loop never needs to ask "have I reached the end?". Returns the position, or -1 if absent."""
    n = len(shelf)
    shelf.append(target)          # the sentinel
    i = 0
    while shelf[i] != target:
        i = i + 1
    shelf.pop()                   # take the sentinel away again
    return i if i < n else -1


def tests_made(shelf: list[int], target: int, sentinel: bool) -> int:
    """How many yes-or-no tests each version makes: the plain loop asks "end?" and "match?" every round;
    the sentinel loop asks only "match?", plus one final "was it the sentinel?"."""
    n = len(shelf)
    if sentinel:
        i = linear_search_sentinel(shelf, target)
        return (n if i == -1 else i) + 1 + 1
    tests = 0
    for i in range(n):
        tests += 2                # end? (no) and match?
        if shelf[i] == target:
            return tests
    return tests + 1              # the final "end?" that stops the loop


def looks_for(shelf: list[int], target: int) -> int:
    """How many items linear search looks at before it stops."""
    i = linear_search(shelf, target)
    return len(shelf) if i == -1 else i + 1


def any_above(values: list[int], limit: int) -> tuple[bool, int]:
    """Is any value above limit? Stops at the first yes (Figure 5.6). Returns (answer, looks)."""
    for looks, v in enumerate(values, start=1):
        if v > limit:
            return True, looks
    return False, len(values)


def all_above(values: list[int], limit: int) -> tuple[bool, int]:
    """Are all values above limit? Stops at the first no (Figure 5.6). Returns (answer, looks)."""
    for looks, v in enumerate(values, start=1):
        if v <= limit:
            return False, looks
    return True, len(values)


if __name__ == "__main__":
    print(running_totals(SHELF))
    counts = [v for _, v in VISITS]
    best, where = max_with_position(counts)
    print("busiest:", VISITS[where][0], best)
    print(linear_search(SHELF, 63), linear_search(SHELF, 50), [looks_for(SHELF, t) for t in (12, 91, 64)])
    print(any_above(SHELF, 80), all_above(SHELF, 20))
