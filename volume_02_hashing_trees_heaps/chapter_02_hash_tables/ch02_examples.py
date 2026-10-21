"""Volume 2, Chapter 2 - Hash Tables.

Run:  python3 ch02_examples.py
"""

from __future__ import annotations

import random


class ChainedTable:
    """Separate chaining with doubling when the load factor would pass 0.75 (Figures 2.1 and 2.4)."""

    def __init__(self, slots: int = 8):
        self.slots: list[list[tuple]] = [[] for _ in range(slots)]
        self.size = 0
        self.resizes = 0

    def _index(self, key) -> int:
        return hash(key) % len(self.slots)

    def put(self, key, value) -> None:
        chain = self.slots[self._index(key)]
        for i, (k, _) in enumerate(chain):
            if k == key:
                chain[i] = (key, value)
                return
        if (self.size + 1) / len(self.slots) > 0.75:
            self._resize()
            chain = self.slots[self._index(key)]
        chain.append((key, value))
        self.size += 1

    def get(self, key, default=None):
        for k, v in self.slots[self._index(key)]:
            if k == key:
                return v
        return default

    def delete(self, key) -> bool:
        chain = self.slots[self._index(key)]
        for i, (k, _) in enumerate(chain):
            if k == key:
                chain.pop(i)
                self.size -= 1
                return True
        return False

    def _resize(self) -> None:
        old = self.slots
        self.slots = [[] for _ in range(2 * len(old))]
        self.resizes += 1
        for chain in old:
            for k, v in chain:
                self.slots[self._index(k)].append((k, v))   # re-hash for the new size


_EMPTY, _TOMB = object(), object()


class ProbingTable:
    """Linear probing with tombstones and doubling (Figure 2.2)."""

    def __init__(self, slots: int = 8):
        self.keys = [_EMPTY] * slots
        self.values = [None] * slots
        self.used = 0                       # live keys + tombstones

    def _probe(self, key):
        i = hash(key) % len(self.keys)
        while True:
            yield i
            i = (i + 1) % len(self.keys)

    def get(self, key, default=None):
        for i in self._probe(key):
            k = self.keys[i]
            if k is _EMPTY:
                return default
            if k is not _TOMB and k == key:
                return self.values[i]

    def put(self, key, value) -> None:
        if (self.used + 1) / len(self.keys) > 0.7:
            self._resize()
        first_tomb = None
        for i in self._probe(key):
            k = self.keys[i]
            if k is _EMPTY:
                target = first_tomb if first_tomb is not None else i
                if first_tomb is None:
                    self.used += 1
                self.keys[target], self.values[target] = key, value
                return
            if k is _TOMB:
                if first_tomb is None:
                    first_tomb = i
            elif k == key:
                self.values[i] = value
                return

    def delete(self, key) -> bool:
        for i in self._probe(key):
            k = self.keys[i]
            if k is _EMPTY:
                return False
            if k is not _TOMB and k == key:
                self.keys[i], self.values[i] = _TOMB, None   # leave a tombstone
                return True

    def _resize(self) -> None:
        old = [(k, v) for k, v in zip(self.keys, self.values) if k is not _EMPTY and k is not _TOMB]
        self.keys = [_EMPTY] * (2 * len(self.keys))
        self.values = [None] * len(self.keys)
        self.used = 0
        for k, v in old:
            self.put(k, v)


def failed_search_probes(alpha: float, m: int = 10_007, searches: int = 3000, seed: int = 1) -> float:
    """Average probes to discover a missing key in a linear-probing table at load factor alpha (Figure 2.3)."""
    rng = random.Random(seed)
    table = [False] * m
    for k in rng.sample(range(10 ** 9), int(alpha * m)):
        i = hash((k, seed)) % m
        while table[i]:
            i = (i + 1) % m
        table[i] = True
    total = 0
    for _ in range(searches):
        i, probes = rng.randrange(m), 1
        while table[i]:
            i, probes = (i + 1) % m, probes + 1
        total += probes
    return total / searches


if __name__ == "__main__":
    for a in (0.1, 0.25, 0.5, 0.75, 0.9):
        print(a, round(failed_search_probes(a), 2), round((1 + 1 / (1 - a) ** 2) / 2, 2))
    t = ChainedTable()
    for i in range(50_000):
        t.put(i, f"title {i}")
    print(t.resizes, len(t.slots), round(t.size / len(t.slots), 2), t.get(31_415))
