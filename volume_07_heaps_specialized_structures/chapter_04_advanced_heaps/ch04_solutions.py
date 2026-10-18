"""Volume 7, Chapter 4 - Solutions to the exercises."""

from __future__ import annotations

import math

from ch04_examples import BinomialHeap, DaryHeap


def dary_height(n: int, d: int) -> int:
    """Exercise 1: levels below the root in a d-ary heap of n items."""
    height, capacity, level_size = 0, 1, 1
    while capacity < n:
        level_size *= d
        capacity += level_size
        height += 1
    return height


def tree_orders(n: int) -> list[int]:
    """Exercise 2: a binomial heap of n items has one tree per 1-bit of n."""
    return [k for k in range(n.bit_length()) if n >> k & 1]


def best_d(pushes: int, pops: int, n: int) -> int:
    """Exercise 3: estimated comparisons = pushes*log_d n + pops*d*log_d n; try d = 2..16."""
    def cost(d: int) -> float:
        levels = math.log(n, d)
        return pushes * levels + pops * d * levels
    return min(range(2, 17), key=cost)


def count_comparisons(d: int, n: int) -> int:
    """Exercise 4: measure push + pop comparisons for n random-ish items."""
    h = DaryHeap(d)
    for i in range(n):
        h.push((i * 7919) % n)
    for _ in range(n):
        h.pop()
    return h.comparisons


if __name__ == "__main__":
    bh = BinomialHeap()
    for x in range(13):
        bh.push(x)
    print(dary_height(1000, 4), tree_orders(13), sorted(bh.trees), best_d(10**6, 10**3, 10**5), count_comparisons(4, 1000))
