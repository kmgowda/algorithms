"""Volume 7, Chapter 11 - Thinking Problems.

Problem 1: an 8-bit register adds exactly modulo 256: wrap(a + b) = wrap(wrap(a) + wrap(b)) (checked for all pairs).
Problem 2: pairwise summation, error growing like log n instead of n, in O(n) additions.
Problem 3: 'add 0.1 until x == 1.0' never stops; the loop with a step count and a tolerance does.
"""

from __future__ import annotations

import math

from ch11_examples import wrap


def pairwise_sum(values: list) -> float:
    """Split in half, sum each half, add the two results."""
    if len(values) <= 2:
        return float(sum(values))
    mid = len(values) // 2
    return pairwise_sum(values[:mid]) + pairwise_sum(values[mid:])


def tenths_until_one(limit: int = 1000) -> tuple[bool, int]:
    """The buggy loop, with a safety limit: does x ever equal 1.0 exactly? Returns (stopped by equality, steps)."""
    x, steps = 0.0, 0
    while x != 1.0 and steps < limit:
        x += 0.1
        steps += 1
    return x == 1.0, steps


def tenths_fixed(stop: float = 1.0, step: float = 0.1) -> int:
    """Count whole steps instead of testing a running float for equality."""
    return round(stop / step)


if __name__ == "__main__":
    big = [1e16] + [1.0] * 10000
    print(pairwise_sum(big) - 1e16, sum(big) - 1e16, tenths_until_one(), tenths_fixed(), wrap(200 + 100))
