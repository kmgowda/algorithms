"""Volume 3, Chapter 20 - Skip Lists.

Run:  python3 ch20_examples.py
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
    """A sorted linked list with express lanes; each node joins lane k with probability 1/2^k (Figure 20.2)."""

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
        """Start in the top lane; move right while the next key is smaller, else drop a lane (Figure 20.3)."""
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

    def delete(self, key) -> list:
        """Remove key if present: find the last node before it on every lane (the update array), unlink the
        node on each lane it belongs to, and drop empty top lanes (Section 20.6). Returns the update array
        as (lane, key before) pairs, top lane first; [] if the key is absent."""
        update, x = [self.head] * MAX_LEVEL, self.head
        for lane in range(self.level - 1, -1, -1):
            while x.next[lane] is not None and x.next[lane].key < key:
                x = x.next[lane]
            update[lane] = x
        target = x.next[0]
        if target is None or target.key != key:
            return []
        before = [(lane, update[lane].key) for lane in range(self.level - 1, -1, -1)]
        for lane in range(len(target.next)):
            update[lane].next[lane] = target.next[lane]          # skip over the deleted node
        while self.level > 1 and self.head.next[self.level - 1] is None:
            self.level -= 1                                      # the top lane is empty: lower the head
        return before

    def range_keys(self, lo, hi) -> list:
        """Every key in lo..hi: search for lo, then walk lane 0 until passing hi (Section 20.9)."""
        x = self.head
        for lane in range(self.level - 1, -1, -1):
            while x.next[lane] is not None and x.next[lane].key < lo:
                x = x.next[lane]
        out, x = [], x.next[0]
        while x is not None and x.key <= hi:
            out.append(x.key)
            x = x.next[0]
        return out

    def lanes(self) -> list[list]:
        out = []
        for lane in range(self.level):
            keys, x = [], self.head.next[lane]
            while x is not None:
                keys.append(x.key)
                x = x.next[lane]
            out.append(keys)
        return out


class VEB:
    """Van Emde Boas tree over the whole numbers 0 .. u - 1 (u a power of 2): insert, member and successor in
    O(log log u). Each node keeps its min and max apart and splits the rest into sqrt(u) clusters plus a summary
    saying which clusters are non-empty."""

    def __init__(self, u: int):
        self.u, self.min, self.max = u, None, None
        if u > 2:
            bits = (u.bit_length() - 1)
            self.lo = 1 << (bits // 2)                  # cluster size
            self.hi = u // self.lo                      # number of clusters
            self.summary, self.cluster = None, {}

    def member(self, x: int) -> bool:
        if x == self.min or x == self.max:
            return True
        if self.u <= 2 or self.min is None:
            return False
        c = self.cluster.get(x // self.lo)
        return c is not None and c.member(x % self.lo)

    def insert(self, x: int) -> None:
        if self.min is None:
            self.min = self.max = x
            return
        if x == self.min or x == self.max:
            return
        if x < self.min:
            x, self.min = self.min, x                   # the new minimum stays here; push the old one down
        if self.u > 2:
            h, l = x // self.lo, x % self.lo
            if h not in self.cluster:
                self.cluster[h] = VEB(self.lo)
                if self.summary is None:
                    self.summary = VEB(self.hi)
                self.summary.insert(h)
            self.cluster[h].insert(l)
        self.max = max(self.max, x)

    def successor(self, x: int):
        """The smallest member greater than x, or None."""
        if self.min is not None and x < self.min:
            return self.min
        if self.u <= 2:
            return self.max if self.max is not None and x < self.max else None
        h, l = x // self.lo, x % self.lo
        c = self.cluster.get(h)
        if c is not None and c.max is not None and l < c.max:
            return h * self.lo + c.successor(l)
        nh = self.summary.successor(h) if self.summary else None
        if nh is None:
            return None
        return nh * self.lo + self.cluster[nh].min


if __name__ == "__main__":
    levels = {12: 1, 25: 3, 31: 1, 47: 2, 58: 4, 63: 1, 70: 2, 84: 3, 91: 1}
    s = SkipList(fixed_levels=levels)
    for k in [12, 25, 31, 47, 58, 63, 70, 84, 91]:
        s.insert(k)
    for lane in reversed(s.lanes()):
        print(lane)
    print(s.search_path(70), s.steps)
    print(s.delete(58), [lane for lane in reversed(s.lanes())])
    big = SkipList(seed=3)
    keys = random.Random(2).sample(range(10 ** 7), 100_000)
    for k in keys:
        big.insert(k)
    total = 0
    for k in keys[:2000]:
        big.search_path(k)
        total += big.steps
    print(big.level, total / 2000, 2 * math.log2(100_000))
