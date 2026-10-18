"""Volume 6, Chapter 6 - Solutions to the exercises."""

from __future__ import annotations

import math
import random

from ch06_examples import build, height


def stick_orders(n: int) -> int:
    """Exercise 1: how many insertion orders of n distinct keys give a height of n - 1? Each new key must be
    the current smallest or largest remaining: 2^(n-1) orders."""
    return 2 ** (n - 1) if n else 0


def average_random_height(n: int, trials: int, seed: int = 0) -> float:
    """Exercise 2: the average height over random insertion orders - it grows in proportion to log n."""
    rng = random.Random(seed)
    total = 0
    for _ in range(trials):
        keys = list(range(n))
        rng.shuffle(keys)
        total += height(build(keys))
    return total / trials


def zigzag_order(n: int) -> list[int]:
    """Exercise 3: an insertion order that is NOT sorted yet still makes a stick: 0, n-1, 1, n-2, 2, ..."""
    lo, hi, out = 0, n - 1, []
    while lo <= hi:
        out.append(lo)
        lo += 1
        if lo <= hi:
            out.append(hi)
            hi -= 1
    return out


def max_steps_ratio(n: int) -> float:
    """Exercise 4: worst search cost in a stick vs. a perfectly balanced tree."""
    return n / (math.floor(math.log2(n)) + 1)


if __name__ == "__main__":
    print(stick_orders(4), round(average_random_height(1000, 20), 1), height(build(zigzag_order(50))), round(max_steps_ratio(10**6)))
