"""Volume 2, Chapter 13 - Hash Tables.

Run:  python3 ch13_examples.py
"""

from __future__ import annotations

import random


class ChainedTable:
    """Separate chaining with doubling when the load factor would pass 0.75 (Figures 13.1 and 13.6)."""

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


def probe_sequence(key, m: int, mode: str = "linear"):
    """The slots tried for key in a table of m slots, m a power of two (Section 13.5, Figure 13.3).

    linear:    home, home + 1, home + 2, ...
    quadratic: home + 0, 1, 3, 6, 10, ... (the triangular numbers, which reach every slot when m is a power of two)
    double:    home, home + step, home + 2 step, ... with an odd step taken from the rest of the hash
    """
    h = hash(key)
    home = h % m
    step = (h // m) % m | 1 if mode == "double" else 1
    for i in range(m):
        if mode == "quadratic":
            yield (home + i * (i + 1) // 2) % m
        else:
            yield (home + i * step) % m


class ProbingTable:
    """Open addressing with tombstones and doubling (Figure 13.2). mode is "linear", "quadratic", or "double"."""

    def __init__(self, slots: int = 8, mode: str = "linear"):
        self.keys = [_EMPTY] * slots
        self.values = [None] * slots
        self.used = 0                       # live keys + tombstones: both count toward the load factor
        self.mode = mode

    def _probe(self, key):
        return probe_sequence(key, len(self.keys), self.mode)

    def get(self, key, default=None):
        for i in self._probe(key):
            k = self.keys[i]
            if k is _EMPTY:
                return default
            if k is not _TOMB and k == key:
                return self.values[i]
        return default

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
        return False

    def _resize(self) -> None:
        old = [(k, v) for k, v in zip(self.keys, self.values) if k is not _EMPTY and k is not _TOMB]
        self.keys = [_EMPTY] * (2 * len(self.keys))     # tombstones are dropped here
        self.values = [None] * len(self.keys)
        self.used = 0
        for k, v in old:
            self.put(k, v)


def failed_search_probes(alpha: float, mode: str = "linear", m: int = 1 << 14, searches: int = 3000,
                         seeds: tuple = (1, 2, 3, 4, 5)) -> float:
    """Average probes to discover a missing key at load factor alpha (Figure 13.5).

    Keys get random homes (and, for double hashing, random odd steps); each search starts from a fresh random
    home. The result is averaged over several seeds, because near alpha = 0.9 one table differs a lot from another.
    """
    total = 0
    for seed in seeds:
        rng = random.Random(seed)
        table = [False] * m

        def slots():
            home, step = rng.randrange(m), rng.randrange(m) | 1
            for i in range(m):
                if mode == "quadratic":
                    yield (home + i * (i + 1) // 2) % m
                elif mode == "double":
                    yield (home + i * step) % m
                else:
                    yield (home + i) % m

        for _ in range(int(alpha * m)):
            for i in slots():
                if not table[i]:
                    table[i] = True
                    break
        for _ in range(searches):
            for probes, i in enumerate(slots(), 1):
                if not table[i]:
                    total += probes
                    break
    return total / (searches * len(seeds))


def division_hash(key: int, m: int) -> int:
    """The division method: the remainder after dividing by m (Section 13.8). Choose m prime."""
    return key % m


def multiplication_hash(key: int, m: int, a: float = 0.6180339887) -> int:
    """The multiplication method: the fractional part of key * A, scaled to m slots (Section 13.8)."""
    return int(m * ((key * a) % 1))


P = 2_147_483_647           # a prime (2**31 - 1) larger than every key used here


def random_universal_hash(m: int, rng: random.Random):
    """Pick one function h(k) = ((a k + b) mod p) mod m from the universal family at random (Section 13.8)."""
    a, b = rng.randrange(1, P), rng.randrange(P)
    return lambda k: ((a * k + b) % P) % m


def collision_rate(x: int, y: int, m: int, trials: int = 20_000, seed: int = 1) -> float:
    """How often two fixed, different keys collide when the function is drawn at random: at most about 1/m."""
    rng = random.Random(seed)
    hits = 0
    for _ in range(trials):
        h = random_universal_hash(m, rng)
        hits += h(x) == h(y)
    return hits / trials


def longest_chain(keys: list[int], m: int, h) -> int:
    """The longest chain a set of keys produces in m slots under hash function h."""
    counts = [0] * m
    for k in keys:
        counts[h(k)] += 1
    return max(counts) if keys else 0


if __name__ == "__main__":
    for a in (0.25, 0.5, 0.75, 0.9):
        print(a, [round(failed_search_probes(a, mode), 2) for mode in ("linear", "quadratic", "double")],
              round((1 + 1 / (1 - a) ** 2) / 2, 2), round(1 / (1 - a), 2))
    t = ChainedTable()
    for i in range(50_000):
        t.put(i, f"title {i}")
    print(t.resizes, len(t.slots), round(t.size / len(t.slots), 2), t.get(31_415))
    calls = [100 + 8 * j for j in range(7)]
    print([division_hash(k, 8) for k in calls], [division_hash(k, 7) for k in calls],
          [multiplication_hash(k, 8) for k in calls])
    attack = [16 * j for j in range(50)]          # keys an attacker picked: all multiples of 16
    print(longest_chain(attack, 16, lambda k: k % 16),
          longest_chain(attack, 16, random_universal_hash(16, random.Random(7))))
    print(collision_rate(100, 116, 16))
    print([list(probe_sequence(k, 16, mode))[:4] for mode in ("linear", "quadratic", "double") for k in (3, 19)])
