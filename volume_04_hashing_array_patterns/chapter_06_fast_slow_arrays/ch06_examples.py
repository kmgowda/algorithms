"""Volume 4, Chapter 6 - Fast and Slow Pointers on Arrays and Sequences.

Run:  python3 ch06_examples.py
"""

from __future__ import annotations

from math import gcd
from typing import Callable


def digit_square_sum(n: int) -> int:
    """19 -> 1*1 + 9*9 = 82."""
    total = 0
    while n:
        n, digit = divmod(n, 10)
        total += digit * digit
    return total


def is_happy(n: int) -> bool:
    """LeetCode 202: repeat digit_square_sum; happy numbers reach 1, others loop forever.

    Floyd's tortoise and hare (V3-C6) detects the loop with O(1) memory - no visited set needed.
    """
    slow, fast = n, digit_square_sum(n)
    while fast != 1 and slow != fast:
        slow = digit_square_sum(slow)
        fast = digit_square_sum(digit_square_sum(fast))
    return fast == 1


def find_cycle(start: int, step: Callable[[int], int]) -> tuple[int, int]:
    """For any sequence x, step(x), step(step(x)), ...: return (where the cycle starts, its length).

    Phase 1: meet inside the cycle. Phase 2: restart one pointer to find the start. Phase 3: measure.
    """
    slow, fast = step(start), step(step(start))
    while slow != fast:
        slow, fast = step(slow), step(step(fast))
    tail_steps, slow = 0, start
    while slow != fast:
        slow, fast = step(slow), step(fast)
        tail_steps += 1
    length, probe = 1, step(slow)
    while probe != slow:
        probe, length = step(probe), length + 1
    return tail_steps, length


def find_duplicate(ids: list[int]) -> int:
    """LeetCode 287: n+1 ids in 1..n, exactly one repeated. Treat i -> ids[i] as 'next' pointers.

    The repeated id is where two arrows point to the same node, i.e. the cycle's entrance.
    O(n) time, O(1) extra space, and the list is not modified.
    """
    slow = fast = ids[0]
    while True:
        slow, fast = ids[slow], ids[ids[fast]]
        if slow == fast:
            break
    slow = ids[0]
    while slow != fast:
        slow, fast = ids[slow], ids[fast]
    return slow


def lcg(seed: int, a: int = 5, c: int = 3, m: int = 16) -> int:
    """A tiny pseudo-random generator: next = (a * x + c) mod m. Real ones are huge; the idea is the same."""
    return (a * seed + c) % m


def shuffle_repeat_period(order: list[int]) -> int:
    """Industry example: a music app applies the same 'shuffle' permutation each time.
    After how many shuffles does the playlist return to the start? (cycle lengths of a permutation)"""
    seen = [False] * len(order)
    period = 1
    for i in range(len(order)):
        if not seen[i]:
            length, j = 0, i
            while not seen[j]:
                seen[j] = True
                j = order[j]
                length += 1
            period = period * length // gcd(period, length)
    return period


if __name__ == "__main__":
    print("19 happy?", is_happy(19), "| 2 happy?", is_happy(2))
    print("Cycle of the digit-square sequence from 2:", find_cycle(2, digit_square_sum))
    print("Duplicate bus pass:", find_duplicate([3, 1, 3, 4, 2]))
    print("LCG (tail, period):", find_cycle(7, lcg), "| with a bad multiplier:", find_cycle(7, lambda x: lcg(x, a=4)))
    print("Shuffle returns after", shuffle_repeat_period([1, 2, 0, 4, 3]), "shuffles")
