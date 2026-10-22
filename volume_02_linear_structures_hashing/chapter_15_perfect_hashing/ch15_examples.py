"""Volume 2, Chapter 15 - Perfect Hashing: the FKS two-level table.

Run:  python3 ch15_examples.py
"""

from __future__ import annotations

import random

SHELF = [12, 25, 31, 47, 58, 63, 70, 84, 91]     # Maya's library shelf, the volume's running keys
P = 101                                            # a prime larger than every shelf key (Section 15.4)


def uh(a: int, b: int, p: int, m: int):
    """One member of the universal family of Chapter 13: k -> ((a k + b) mod p) mod m."""
    return lambda k: ((a * k + b) % p) % m


def bucket_sizes(keys, a: int, b: int, p: int, m: int) -> list[int]:
    """How many keys the primary function sends to each of the m buckets."""
    sizes = [0] * m
    f = uh(a, b, p, m)
    for k in keys:
        sizes[f(k)] += 1
    return sizes


def build_secondary(bucket, p: int, rng: random.Random):
    """A collision-free table of len(bucket)**2 slots for one bucket (Section 15.5).

    Returns (a, b, slots, tries): random functions are drawn until none of the keys collide.
    """
    s = len(bucket) ** 2
    tries = 0
    while True:
        tries += 1
        a, b = rng.randrange(1, p), rng.randrange(p)
        slots = [None] * s
        f = uh(a, b, p, s)
        for k in bucket:
            if slots[f(k)] is not None:
                break                                  # a collision: draw another function
            slots[f(k)] = k
        else:
            return a, b, slots, tries


class PerfectTable:
    """The FKS scheme for a fixed set of keys: worst-case O(1) find, O(n) expected space (Figures 15.3 to 15.5).

    Duplicate keys are ignored (a set has each key once). Keys must be whole numbers below p.
    """

    def __init__(self, keys, p: int = P, seed: int = 1):
        self.keys = list(dict.fromkeys(keys))
        if any(not 0 <= k < p for k in self.keys):
            raise ValueError("keys must lie in 0 .. p - 1")
        self.p, self.m = p, len(self.keys)
        rng = random.Random(seed)
        self.primary_tries, self.secondary_tries = 0, []
        self.a = self.b = 0
        self.buckets: list = []
        if self.m == 0:
            return
        while True:                                    # step 1: a primary function with small sum of squares
            self.primary_tries += 1
            self.a, self.b = rng.randrange(1, p), rng.randrange(p)
            if sum(s * s for s in bucket_sizes(self.keys, self.a, self.b, p, self.m)) < 4 * self.m:
                break
        f = uh(self.a, self.b, p, self.m)
        groups = [[] for _ in range(self.m)]
        for k in self.keys:
            groups[f(k)].append(k)
        for g in groups:                               # step 2: one collision-free table per bucket
            if not g:
                self.buckets.append(None)
                self.secondary_tries.append(0)
                continue
            a, b, slots, tries = build_secondary(g, p, rng)
            self.buckets.append((a, b, slots))
            self.secondary_tries.append(tries)

    def find(self, key) -> bool:
        if self.m == 0 or not 0 <= key < self.p:
            return False
        bucket = self.buckets[uh(self.a, self.b, self.p, self.m)(key)]
        if bucket is None:
            return False
        a, b, slots = bucket
        return slots[uh(a, b, self.p, len(slots))(key)] == key

    def space(self) -> int:
        """Slots of the primary table plus all secondary slots."""
        return self.m + sum(len(bkt[2]) for bkt in self.buckets if bkt)


def collision_free_rate(n: int, s: int, trials: int = 20_000, seed: int = 3) -> float:
    """How often n random keys hashed into s slots have no collision at all (Figure 15.2)."""
    rng = random.Random(seed)
    good = 0
    for _ in range(trials):
        seen = set()
        for _ in range(n):
            x = rng.randrange(s)
            if x in seen:
                break
            seen.add(x)
        else:
            good += 1
    return good / trials


def space_experiment(n: int, trials: int = 200, seed: int = 5, p: int = 2_147_483_647) -> tuple[float, float]:
    """Average sum of squares of the bucket sizes for a random primary function with m = n buckets, and the share
    of functions accepted by the rule sum < 4n (Section 15.7)."""
    rng = random.Random(seed)
    keys = rng.sample(range(1, p), n)
    total, accepted = 0, 0
    for _ in range(trials):
        sq = sum(s * s for s in bucket_sizes(keys, rng.randrange(1, p), rng.randrange(p), p, n))
        total += sq
        accepted += sq < 4 * n
    return total / trials, accepted / trials


def compare(keys=SHELF, m: int = 11) -> dict:
    """Worst successful probes and total slots for chaining, linear probing (h = k mod m) and FKS (Figure 15.7)."""
    chains = [[] for _ in range(m)]
    for k in keys:
        chains[k % m].append(k)
    slots = [None] * m
    worst_lp = 0
    for k in keys:
        i, probes = k % m, 1
        while slots[i] is not None:
            i, probes = (i + 1) % m, probes + 1
        slots[i] = k
        worst_lp = max(worst_lp, probes)
    t = PerfectTable(keys)
    return {"chaining": (max(len(c) for c in chains), m + len(keys)),
            "linear probing": (worst_lp, m),
            "cuckoo": (2, 2 * m),
            "perfect (FKS)": (2, t.space())}


if __name__ == "__main__":
    t = PerfectTable(SHELF)
    print("primary a, b =", t.a, t.b, "tries", t.primary_tries)
    for j, bkt in enumerate(t.buckets):
        print(j, bkt, t.secondary_tries[j])
    print("space", t.space(), compare())
