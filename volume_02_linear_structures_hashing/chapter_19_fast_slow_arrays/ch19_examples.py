"""Volume 2, Chapter 19 - Fast and Slow Pointers on Arrays.

Run:  python3 ch19_examples.py
"""

from __future__ import annotations

import random


def find_duplicate(a: list[int]) -> int:
    """A value repeated in a list of n + 1 numbers from 1..n, with O(1) extra memory (Figure 19.3)."""
    slow = fast = a[0]
    while True:                     # phase 1: meet inside the loop
        slow, fast = a[slow], a[a[fast]]
        if slow == fast:
            break
    slow = a[0]
    while slow != fast:             # phase 2: walk together to the entrance
        slow, fast = a[slow], a[fast]
    return slow


def cycle_entrance(a: list[int], start: int = 0) -> int:
    """Floyd's two phases from any start position, as in the pseudocode of Section 19.5.

    From position 0 (which no value names) the answer is the repeated value; from a start on the loop
    the walkers simply meet at the start again (Practice Problem 19.4)."""
    slow, fast = a[start], a[a[start]]
    while slow != fast:
        slow, fast = a[slow], a[a[fast]]
    slow = start
    while slow != fast:
        slow, fast = a[slow], a[fast]
    return slow


def digit_square_sum(n: int) -> int:
    return sum(int(d) ** 2 for d in str(n))


def is_happy(n: int) -> bool:
    """Tortoise and hare on the digit-square sequence (Figure 19.4)."""
    slow, fast = n, digit_square_sum(n)
    while fast != 1 and slow != fast:
        slow = digit_square_sum(slow)
        fast = digit_square_sum(digit_square_sum(fast))
    return fast == 1


def ticket_log(n: int, seed: int = 1) -> list[int]:
    """Section 19.8: n + 1 tickets numbered 1..n, one number issued twice, in random order."""
    rng = random.Random(seed)
    log = list(range(1, n + 1)) + [rng.randint(1, n)]
    rng.shuffle(log)
    return log


if __name__ == "__main__":
    print(find_duplicate([3, 1, 3, 4, 2]), find_duplicate([1, 3, 4, 2, 2]))
    print([n for n in range(1, 50) if is_happy(n)], is_happy(19), is_happy(4), is_happy(7))
    log = ticket_log(500)
    print(find_duplicate(log))
