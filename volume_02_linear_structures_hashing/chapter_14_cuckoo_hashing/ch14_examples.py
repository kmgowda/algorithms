"""Volume 2, Chapter 14 - Cuckoo Hashing (with Robin Hood hashing as a comparison).

Run:  python3 ch14_examples.py
"""

from __future__ import annotations

import random

SHELF = [12, 25, 31, 47, 58, 63, 70, 84, 91]     # Maya's library shelf, the volume's running keys
P = 2_147_483_647                                  # a prime larger than every key, as in Chapter 13


def h1(key: int, m: int) -> int:
    """First home: the remainder after dividing by m (Section 14.4)."""
    return key % m


def h2(key: int, m: int) -> int:
    """Second home: the next digit up in base m (Section 14.4)."""
    return (key // m) % m


class CuckooTable:
    """Two tables; every key lives in T[0][f0(key)] or T[1][f1(key)] (Figures 14.2 to 14.5).

    With hashes=None the two functions are the fixed h1 and h2 of the chapter's figures; with hashes="random" each
    rebuild draws two fresh functions ((a k + b) mod p) mod m from the universal family of Chapter 13.
    """

    def __init__(self, m: int = 11, hashes=None, seed: int = 1, max_kicks: int | None = None):
        self.m, self.mode, self.rng = m, hashes, random.Random(seed)
        self.max_kicks = max_kicks
        self.size, self.rehashes, self.kicks = 0, 0, 0
        self.log: list[tuple] = []                 # (key placed, table, slot) for every move, for the figures
        self._new_functions()
        self.T = [[None] * m, [None] * m]

    def _new_functions(self) -> None:
        if self.mode == "random":
            pairs = [(self.rng.randrange(1, P), self.rng.randrange(P)) for _ in range(2)]
            self.f = [lambda k, a=a, b=b: ((a * k + b) % P) % self.m for a, b in pairs]
        else:
            self.f = [lambda k: h1(k, self.m), lambda k: h2(k, self.m)]

    def limit(self) -> int:
        """How many evictions an insert may cause before it gives up and rebuilds."""
        if self.max_kicks is not None:
            return self.max_kicks
        return max(8, 6 * self.m.bit_length())

    def find(self, key) -> bool:
        return self.T[0][self.f[0](key)] == key or self.T[1][self.f[1](key)] == key

    def delete(self, key) -> bool:
        for t in (0, 1):
            i = self.f[t](key)
            if self.T[t][i] == key:
                self.T[t][i] = None
                self.size -= 1
                return True
        return False

    def insert(self, key) -> None:
        if self.find(key):
            return
        if (self.size + 1) / (2 * self.m) > 0.5:     # keep each table at most half full
            self._rebuild(2 * self.m)
        x = self._place(key)
        while x is not None:                          # an eviction chain failed: new functions, try again
            self._rebuild(self.m)
            x = self._place(x)
        self.size += 1

    def _place(self, x):
        """Walk the eviction chain for x. Return None on success, or the key left homeless."""
        t = 0
        for _ in range(self.limit()):
            i = self.f[t](x)
            x, self.T[t][i] = self.T[t][i], x        # put x in its nest; pick up whoever lived there
            self.log.append((self.T[t][i], t, i))
            if x is None:
                return None
            self.kicks += 1
            t = 1 - t                                 # the evicted key goes to its home in the other table
        return x

    def _rebuild(self, m: int) -> None:
        keys = [k for row in self.T for k in row if k is not None]
        while True:
            self.m, self.rehashes = m, self.rehashes + 1
            if self.mode is None:
                self.mode = "random"                  # the fixed pair failed; switch to random functions
            self._new_functions()
            self.T = [[None] * m, [None] * m]
            if all(self._place(k) is None for k in keys):
                return

    def keys(self) -> list:
        return [k for row in self.T for k in row if k is not None]


def cuckoo_insert(T, f, x, max_kicks):
    """The insert loop of Section 14.4 on its own: T is two lists, f two hash functions.

    Returns (None, moves) on success, or (homeless key, moves) when the chain is too long.
    """
    moves, t = 0, 0
    for _ in range(max_kicks):
        i = f[t](x)
        x, T[t][i] = T[t][i], x
        moves += 1
        if x is None:
            return None, moves
        t = 1 - t
    return x, moves


def cuckoo_graph_has_room(keys, f0, f1, m: int) -> bool:
    """True when every key can be placed: each connected piece of the cuckoo graph (slots as dots, keys as lines
    joining their two homes) has no more keys than slots (Section 14.6)."""
    parent = list(range(2 * m))
    slots, edges = [1] * (2 * m), [0] * (2 * m)

    def root(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    for k in keys:
        a, b = root(f0(k)), root(m + f1(k))
        if a != b:
            parent[b] = a
            slots[a] += slots[b]
            edges[a] += edges[b]
        edges[a] += 1
    return all(edges[v] <= slots[v] for v in range(2 * m) if root(v) == v)


class RobinHoodTable:
    """Linear probing in which a key that has travelled further takes the slot of one that has travelled less
    (Section 14.8). Distances are counted from each key's home h1(key, m)."""

    def __init__(self, m: int = 11):
        self.m = m
        self.slots: list = [None] * m             # (key, distance from home) or None

    def insert(self, key) -> None:
        d = 0
        i = h1(key, self.m)
        while True:
            here = self.slots[i]
            if here is None:
                self.slots[i] = (key, d)
                return
            if here[0] == key:
                return
            if here[1] < d:                        # the resident is "richer": swap and carry it on
                self.slots[i], (key, d) = (key, d), here
            i, d = (i + 1) % self.m, d + 1

    def find(self, key) -> int:
        """Probes used to find key, or minus the probes used to prove it absent."""
        i, d = h1(key, self.m), 0
        while True:
            here = self.slots[i]
            if here is None or here[1] < d:        # an empty slot, or a richer key: key cannot be further on
                return -(d + 1)
            if here[0] == key:
                return d + 1
            i, d = (i + 1) % self.m, d + 1


def chain_buckets(keys, m: int) -> list[list]:
    """Separate chaining with h1, as in Chapter 13."""
    buckets = [[] for _ in range(m)]
    for k in keys:
        buckets[h1(k, m)].append(k)
    return buckets


def linear_probe_slots(keys, m: int) -> list:
    """Plain linear probing with h1, as in Chapter 13."""
    slots = [None] * m
    for k in keys:
        i = h1(k, m)
        while slots[i] is not None:
            i = (i + 1) % m
        slots[i] = k
    return slots


def probes_linear(slots, key, m: int) -> int:
    """Probes to find key, or (negative) to prove it absent, in a plain linear-probing table."""
    i, n = h1(key, m), 1
    while slots[i] is not None:
        if slots[i] == key:
            return n
        i, n = (i + 1) % m, n + 1
        if n > m:
            break
    return -n


def compare(keys=SHELF, m: int = 11) -> dict:
    """Probes per successful search (average, worst) and worst failed search for the four designs (Figure 14.8)."""
    out = {}
    b = chain_buckets(keys, m)
    hit = [b[h1(k, m)].index(k) + 1 for k in keys]
    miss = [max(1, len(c)) for c in b]             # every key on the chain; an empty slot is one look
    out["chaining"] = (sum(hit) / len(keys), max(hit), max(miss), m)
    s = linear_probe_slots(keys, m)
    hit = [probes_linear(s, k, m) for k in keys]
    miss = [-probes_linear(s, k, m) for k in absent_homes(keys, m)]
    out["linear"] = (sum(hit) / len(keys), max(hit), max(miss), m)
    s = linear_probe_slots(keys, 2 * m)
    hit = [probes_linear(s, k, 2 * m) for k in keys]
    miss = [-probes_linear(s, k, 2 * m) for k in absent_homes(keys, 2 * m)]
    out["linear, double space"] = (sum(hit) / len(keys), max(hit), max(miss), 2 * m)
    rh = RobinHoodTable(m)
    for k in keys:
        rh.insert(k)
    hit = [rh.find(k) for k in keys]
    miss = [-rh.find(k) for k in absent_homes(keys, m)]
    out["robin hood"] = (sum(hit) / len(keys), max(hit), max(miss), m)
    c = CuckooTable(m)
    for k in keys:
        c.insert(k)
    hit = [1 if c.T[0][c.f[0](k)] == k else 2 for k in keys]
    out["cuckoo"] = (sum(hit) / len(keys), max(hit), 2, 2 * m)
    return out


def absent_homes(keys, m: int) -> list[int]:
    """One absent key for every home slot 0..m-1 (a failed search can start anywhere)."""
    out = []
    for home in range(m):
        k = home
        while k in keys:
            k += m
        out.append(k)
    return out


def insert_cost_experiment(n: int, load: float, trials: int = 20, seed: int = 7) -> tuple[float, int]:
    """Average evictions per insert (rebuild work included), and the number of rebuilds, when n random keys go
    into two tables of n / (2 load) slots each, with no growing (Figure 14.7). Keep load at or below 0.5."""
    rng = random.Random(seed)
    total, rebuilds = 0, 0
    for t in range(trials):
        m = max(2, int(n / (2 * load)))
        table = CuckooTable(m, hashes="random", seed=seed + t)
        table.max_kicks = max(8, 6 * m.bit_length())
        keys = rng.sample(range(1, 10**9), n)
        for k in keys:
            x = table._place(k)
            while x is not None:
                table._rebuild(m)
                x = table._place(x)
            table.size += 1
        total += table.kicks
        rebuilds += table.rehashes
    return total / (n * trials), rebuilds


if __name__ == "__main__":
    c = CuckooTable(11)
    for k in SHELF:
        c.insert(k)
    print("T1:", c.T[0])
    print("T2:", c.T[1])
    for name, row in compare().items():
        print(name, row)
