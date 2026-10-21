"""Volume 2, Chapter 31 - Skip Lists.

Run:  python3 ch31_examples.py
"""

from __future__ import annotations

import math
import random

MAX_LEVEL = 32


class _Node:
    __slots__ = ("key", "next")

    def __init__(self, key, levels):
        self.key, self.next = key, [None] * levels


class SkipList:
    """A sorted linked list with express lanes; each node joins lane k with probability 1/2^k (Figure 31.2)."""

    def __init__(self, seed: int = 1, fixed_levels: dict | None = None):
        self.head = _Node(None, MAX_LEVEL)
        self.level = 1
        self.rng = random.Random(seed)
        self.fixed = fixed_levels or {}
        self.steps = 0

    def _random_level(self, key) -> int:
        if key in self.fixed:
            return self.fixed[key]
        lvl = 1
        while lvl < MAX_LEVEL and self.rng.random() < 0.5:     # flip a coin for each higher lane
            lvl += 1
        return lvl

    def search_path(self, key) -> list:
        """Start in the top lane; move right while the next key is smaller, else drop a lane (Figure 31.3)."""
        path, x = [], self.head
        self.steps = 0
        for lane in range(self.level - 1, -1, -1):
            while x.next[lane] is not None and x.next[lane].key < key:
                x = x.next[lane]
                path.append((lane, x.key))
                self.steps += 1
            self.steps += 1
        return path

    def contains(self, key) -> bool:
        self.search_path(key)
        x = self.head
        for lane in range(self.level - 1, -1, -1):
            while x.next[lane] is not None and x.next[lane].key < key:
                x = x.next[lane]
        x = x.next[0]
        return x is not None and x.key == key

    def insert(self, key) -> None:
        update, x = [self.head] * MAX_LEVEL, self.head
        for lane in range(self.level - 1, -1, -1):
            while x.next[lane] is not None and x.next[lane].key < key:
                x = x.next[lane]
            update[lane] = x
        if x.next[0] is not None and x.next[0].key == key:
            return
        lvl = self._random_level(key)
        self.level = max(self.level, lvl)
        node = _Node(key, lvl)
        for lane in range(lvl):
            node.next[lane], update[lane].next[lane] = update[lane].next[lane], node

    def lanes(self) -> list[list]:
        out = []
        for lane in range(self.level):
            keys, x = [], self.head.next[lane]
            while x is not None:
                keys.append(x.key)
                x = x.next[lane]
            out.append(keys)
        return out


if __name__ == "__main__":
    levels = {12: 1, 25: 3, 31: 1, 47: 2, 58: 4, 63: 1, 70: 2, 84: 3, 91: 1}
    s = SkipList(fixed_levels=levels)
    for k in [12, 25, 31, 47, 58, 63, 70, 84, 91]:
        s.insert(k)
    for lane in reversed(s.lanes()):
        print(lane)
    print(s.search_path(70), s.steps)
    big = SkipList(seed=3)
    keys = random.Random(2).sample(range(10 ** 7), 100_000)
    for k in keys:
        big.insert(k)
    total = 0
    for k in keys[:2000]:
        big.search_path(k)
        total += big.steps
    print(big.level, total / 2000, 2 * math.log2(100_000))
