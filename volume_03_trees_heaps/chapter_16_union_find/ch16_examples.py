"""Volume 3, Chapter 16 - Union-Find (Disjoint Sets).

Run:  python3 ch16_examples.py
"""

from __future__ import annotations

import random


class UnionFind:
    """Each group is a tree of parent pointers; the root names the group (Figures 16.2, 16.4 and 16.6)."""

    def __init__(self, items):
        self.parent = {x: x for x in items}
        self.size = {x: 1 for x in items}
        self.groups = len(self.parent)

    def find(self, x):
        """Follow parents to the root, then point every visited member straight at it (path compression)."""
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, a, b) -> bool:
        """Join the groups of a and b; the smaller tree hangs under the larger root (union by size)."""
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.groups -= 1
        return True

    def same(self, a, b) -> bool:
        return self.find(a) == self.find(b)


class NaiveUnionFind:
    """Quick-union: no balancing, no compression, so trees can grow into long chains (Figure 16.3, panel 2)."""

    def __init__(self, items):
        self.parent = {x: x for x in items}

    def find(self, x):
        steps = 0
        while self.parent[x] != x:
            x = self.parent[x]
            steps += 1
        return x, steps

    def union(self, a, b):
        ra, rb = self.find(a)[0], self.find(b)[0]
        if ra != rb:
            self.parent[ra] = rb


def depth(uf_parent: dict, x) -> int:
    d = 0
    while uf_parent[x] != x:
        x, d = uf_parent[x], d + 1
    return d


def connect_routes(n: int, routes) -> tuple[list, int | None]:
    """Section 16.9: returns (redundant routes, index of the route after which all branches connect)."""
    uf = UnionFind(range(1, n + 1))
    redundant, connected_at = [], None
    for i, (a, b) in enumerate(routes):
        if not uf.union(a, b):
            redundant.append((a, b))
        if uf.groups == 1 and connected_at is None:
            connected_at = i
    return redundant, connected_at


class QuickFind:
    """Every member carries its group's label: find is one look-up, but union relabels a whole group (Section 16.5)."""

    def __init__(self, items):
        self.label = {x: x for x in items}
        self.writes = 0                       # label changes, the cost of union

    def find(self, x):
        return self.label[x]

    def union(self, a, b) -> bool:
        la, lb = self.label[a], self.label[b]
        if la == lb:
            return False
        for x in self.label:                  # scan everyone: O(n) per union
            if self.label[x] == la:
                self.label[x] = lb
                self.writes += 1
        return True


class UnionByRank:
    """Union by rank with path halving (Sections 16.6 and 16.7). A rank is an upper bound on a root's height."""

    def __init__(self, items):
        self.parent = {x: x for x in items}
        self.rank = {x: 0 for x in items}

    def find(self, x):
        """Path halving: every node on the path skips to its grandparent, in one pass."""
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra                  # the lower rank goes under the higher
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1                # only equal ranks make the tree taller
        return True


def min_members_by_rank(max_rank: int) -> list[int]:
    """Smallest group that can reach each rank under union by rank: always 2 ** r (the rank lemma)."""
    best = {0: 1}
    for r in range(1, max_rank + 1):
        best[r] = 2 * best[r - 1]             # a rank-r root needs two rank-(r-1) roots joined
    return [best[r] for r in range(max_rank + 1)]


def ackermann_level(k: int, j: int, cap: int) -> int:
    """A_k(j), capped at cap: A_0(j) = j + 1, and A_k(j) applies A_(k-1) to j, j + 1 times over (CLRS, Section 19.4)."""
    if k == 0:
        return min(j + 1, cap)
    if k == 1:
        return min(2 * j + 1, cap)                        # closed form of A_1
    if k == 2:
        return cap if j >= cap.bit_length() else min(2 ** (j + 1) * (j + 1) - 1, cap)   # closed form of A_2
    x = j
    for _ in range(j + 1):
        x = ackermann_level(k - 1, x, cap)
        if x >= cap:
            return cap
    return x


def inverse_ackermann(n: int) -> int:
    """alpha(n): the smallest k with A_k(1) >= n. It is at most 4 for any n up to 10**80 and far beyond."""
    k = 0
    while ackermann_level(k, 1, n) < n:
        k += 1
    return k

if __name__ == "__main__":
    print(connect_routes(6, [(1, 2), (2, 3), (4, 5), (3, 1), (5, 6), (3, 4)]))
    people = ["Ana", "Ben", "Cai", "Dev", "Eva", "Fay", "Gus"]
    uf = UnionFind(people)
    for a, b in [("Ana", "Ben"), ("Cai", "Dev"), ("Eva", "Fay"), ("Ben", "Dev"), ("Gus", "Fay")]:
        uf.union(a, b)
        print(a, b, uf.groups, dict(uf.parent))
    print(uf.same("Ana", "Cai"), uf.same("Ana", "Eva"))
    n = 10_000
    naive = NaiveUnionFind(range(n))
    for i in range(n - 1):
        naive.union(i, i + 1)
    print("naive depth of 0:", naive.find(0)[1])
    good = UnionFind(range(n))
    for i in range(n - 1):
        good.union(i, i + 1)
    print("balanced max depth:", max(depth(good.parent, i) for i in range(n)))
    rng = random.Random(1)
    big = UnionFind(range(100_000))
    for _ in range(200_000):
        big.union(rng.randrange(100_000), rng.randrange(100_000))
    print("random unions max depth:", max(depth(big.parent, i) for i in range(0, 100_000, 7)), big.groups)
    qf = QuickFind(range(n))
    for i in range(n - 1):
        qf.union(i, i + 1)
    print("quick-find label writes for a line of 10,000:", qf.writes)
    rk = UnionByRank(range(100_000))
    rng = random.Random(1)
    for _ in range(200_000):
        rk.union(rng.randrange(100_000), rng.randrange(100_000))
    print("highest rank after 200,000 random unions:", max(rk.rank.values()))
    print("alpha:", [(m, inverse_ackermann(m)) for m in (2, 3, 7, 2047, 2048, 10 ** 80)])
