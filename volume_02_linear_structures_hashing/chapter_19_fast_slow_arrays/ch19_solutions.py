"""Volume 2, Chapter 19 - Thinking Problem solutions (Section 19.16)."""

from __future__ import annotations


def tail_and_loop(a: list[int], start: int = 0) -> tuple[int, int]:
    """Thinking Problem 19.2: (tail length t, loop length c) of the walk i -> a[i] from start.

    Every value must be a position 0..len(a) - 1. O(t + c) jumps, O(1) extra memory;
    the hunt opens exactly t + c different lockers."""
    slow, fast = a[start], a[a[start]]
    while slow != fast:                   # phase 1: meet inside the loop
        slow, fast = a[slow], a[a[fast]]
    slow, t = start, 0
    while slow != fast:                   # phase 2: count the tail
        slow, fast, t = a[slow], a[fast], t + 1
    c, walker = 1, a[slow]
    while walker != slow:                 # phase 3: walk once round the loop
        walker, c = a[walker], c + 1
    return t, c


def find_duplicate_mixed(a: list[int], max_rounds: int = 10_000) -> int | None:
    """Thinking Problem 19.3: the buggy mix of the two conventions (phase 1 from a[0], phase 2 from 0).

    Returns None when phase 2 has not met after max_rounds rounds (it never will when the loop is longer than 1)."""
    slow = fast = a[0]
    while True:
        slow, fast = a[slow], a[a[fast]]
        if slow == fast:
            break
    slow = 0
    for _ in range(max_rounds):
        if slow == fast:
            return slow
        slow, fast = a[slow], a[fast]
    return None
