"""Volume 14, Chapter 7 - Solutions to the exercises."""

from __future__ import annotations

import random


def random_pick_index(nums: list[int], target: int, rng: random.Random) -> int:
    """Exercise 1 (LeetCode 398): a uniformly random index of target, one pass - reservoir sampling with k = 1."""
    chosen, seen = -1, 0
    for i, v in enumerate(nums):
        if v == target:
            seen += 1
            if rng.randint(1, seen) == 1:
                chosen = i
    return chosen


def coupon_collector(n: int) -> float:
    """Exercise 2: expected draws to collect all n coupons = n x (1 + 1/2 + ... + 1/n)."""
    return n * sum(1 / k for k in range(1, n + 1))


def weighted_choice(weights: dict[str, int], rng: random.Random) -> str:
    """Exercise 3 (LeetCode 528 idea): pick a key with probability proportional to its weight."""
    r = rng.uniform(0, sum(weights.values()))
    running = 0.0
    for key, w in weights.items():
        running += w
        if r <= running:
            return key
    return key


if __name__ == "__main__":
    rng = random.Random(0)
    print(random_pick_index([1, 2, 3, 3, 3], 3, rng), round(coupon_collector(6), 2), weighted_choice({"a": 1, "b": 3}, rng))
