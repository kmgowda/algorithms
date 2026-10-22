"""Volume 2, Chapter 12 - Thinking Problems.

Problem 1: for any hash into m slots, (n - 1) * m + 1 keys force n keys into one slot (checked on small cases).
Problem 2: find two labels that collide in O(sqrt(m)) expected tries, by the birthday bound.
Problem 3: the chance of no collision, exactly and by the bound of Theorem 12.1.
"""

from __future__ import annotations

import math
import random

from ch12_examples import multiply_add_hash


def crowded_slot(keys: list[str], m: int, fn=multiply_add_hash) -> tuple[int, int]:
    """The fullest slot and how many keys it holds."""
    counts = [0] * m
    for k in keys:
        counts[fn(k, m)] += 1
    best = max(range(m), key=counts.__getitem__)
    return best, counts[best]


def find_collision(m: int, seed: int = 12, fn=multiply_add_hash) -> tuple[str, str, int]:
    rng = random.Random(seed)
    owner: dict[int, str] = {}                  # slot -> the first label seen there
    tries = 0
    while True:
        label = "".join(rng.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(8))
        tries += 1
        slot = fn(label, m)
        if slot in owner and owner[slot] != label:
            return owner[slot], label, tries
        owner[slot] = label


def no_collision_chance(n: int, m: int) -> float:
    return math.prod((m - i) / m for i in range(n))


def no_collision_bound(n: int, m: int) -> float:
    return math.exp(-n * (n - 1) / (2 * m))


if __name__ == "__main__":
    print(find_collision(65_536))
    print(round(no_collision_chance(2000, 10**6), 3), round(no_collision_bound(2000, 10**6), 3))
