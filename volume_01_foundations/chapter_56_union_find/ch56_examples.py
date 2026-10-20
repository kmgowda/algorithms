"""Volume 1, Chapter 56 - Union-Find (Disjoint Sets).

Run:  python3 ch56_examples.py
"""

from __future__ import annotations

import random


class UnionFind:
    """Each group is a tree of parent pointers; the root names the group (Figures 56.2 to 56.4)."""

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
    """No balancing, no compression: trees can grow into long chains."""

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
    """Section 56.9: returns (redundant routes, index of the route after which all branches connect)."""
    uf = UnionFind(range(1, n + 1))
    redundant, connected_at = [], None
    for i, (a, b) in enumerate(routes):
        if not uf.union(a, b):
            redundant.append((a, b))
        if uf.groups == 1 and connected_at is None:
            connected_at = i
    return redundant, connected_at


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
