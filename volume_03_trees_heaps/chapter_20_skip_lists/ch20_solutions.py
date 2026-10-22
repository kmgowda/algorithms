"""Volume 3, Chapter 20 - Skip Lists: companion code for the Thinking Problems (Section 20.17).

Run:  python3 ch20_solutions.py
"""

from __future__ import annotations

import math
import random

from ch20_examples import MAX_LEVEL, SkipList


def average_lanes(n: int, trials: int = 200, seed: int = 1) -> float:
    """Thinking Problem 1: the average number of lanes of a skip list of n random heights."""
    rng, total = random.Random(seed), 0
    for _ in range(trials):
        top = 0
        for _ in range(n):
            lvl = 1
            while lvl < MAX_LEVEL and rng.random() < 0.5:
                lvl += 1
            top = max(top, lvl)
        total += top
    return total / trials


def lane_bound(n: int) -> int:
    """Thinking Problem 1: the proved bound on the expected number of lanes, ceil(log2 n) + 2."""
    return math.ceil(math.log2(n)) + 2


class _WNode:
    __slots__ = ("key", "next", "width")

    def __init__(self, key, levels):
        self.key, self.next, self.width = key, [None] * levels, [1] * levels


class RankSkipList(SkipList):
    """Thinking Problem 2: each link also stores its width, the number of lane-0 steps it covers."""

    def __init__(self, seed: int = 1, fixed_levels: dict | None = None):
        super().__init__(seed, fixed_levels)
        self.head, self.size = _WNode(None, MAX_LEVEL), 0

    def _walk(self, key):
        """The update array and the rank of each update node (the head has rank 0)."""
        update, rank, x, r = [self.head] * MAX_LEVEL, [0] * MAX_LEVEL, self.head, 0
        for lane in range(self.level - 1, -1, -1):
            while x.next[lane] is not None and x.next[lane].key < key:
                r += x.width[lane]
                x = x.next[lane]
            update[lane], rank[lane] = x, r
        return update, rank, x.next[0]

    def insert(self, key) -> None:
        update, rank, nxt = self._walk(key)
        if nxt is not None and nxt.key == key:
            return
        lvl = self._random_level(key)
        self.level = max(self.level, lvl)
        node, r = _WNode(key, lvl), rank[0] + 1                 # the new key's rank
        for lane in range(self.level):
            u = update[lane]
            if lane < lvl:                                       # split u's link in two
                node.next[lane], u.next[lane] = u.next[lane], node
                node.width[lane] = rank[lane] + u.width[lane] + 1 - r
                u.width[lane] = r - rank[lane]
            elif u.next[lane] is not None:                       # the link now jumps over one more key
                u.width[lane] += 1
        self.size += 1

    def delete(self, key) -> bool:
        update, rank, target = self._walk(key)
        if target is None or target.key != key:
            return False
        for lane in range(self.level):
            u = update[lane]
            if lane < len(target.next):                          # join the two links around target
                u.width[lane] += target.width[lane] - 1
                u.next[lane] = target.next[lane]
            elif u.next[lane] is not None:
                u.width[lane] -= 1
        while self.level > 1 and self.head.next[self.level - 1] is None:
            self.level -= 1
        self.size -= 1
        return True

    def kth(self, k: int):
        """The k-th smallest key (k = 1 is the smallest), or None. O(log n) expected."""
        if not 1 <= k <= self.size:
            return None
        x, r = self.head, 0
        for lane in range(self.level - 1, -1, -1):
            while x.next[lane] is not None and r + x.width[lane] <= k:
                r += x.width[lane]
                x = x.next[lane]
        return x.key


def counter_heights(keys: list) -> SkipList:
    """Thinking Problem 3, the bug: the i-th inserted key gets height 1 + (trailing zero bits of i)."""
    levels = {}
    for i, k in enumerate(keys, start=1):
        levels[k] = min(MAX_LEVEL, 1 + ((i & -i).bit_length() - 1))
    s = SkipList(fixed_levels=levels)
    for k in keys:
        s.insert(k)
    return s


if __name__ == "__main__":
    for n in (10, 1000, 100_000):
        print(n, lane_bound(n), average_lanes(n, trials=50))
    t = RankSkipList(seed=4)
    for k in [58, 25, 91, 12, 70, 47, 84, 31, 63]:
        t.insert(k)
    print([t.kth(i) for i in range(1, 10)])
    n = 1000
    keys = [x for i in range(n // 2) for x in (i, 10_000 + i)]
    bad = counter_heights(keys)
    bad.search_path(n // 2 - 1)
    good = SkipList(seed=1)
    for k in keys:
        good.insert(k)
    good.search_path(n // 2 - 1)
    tidy = counter_heights(list(range(n)))
    tidy.search_path(n // 2 - 1)
    print(bad.steps, good.steps, tidy.steps)
