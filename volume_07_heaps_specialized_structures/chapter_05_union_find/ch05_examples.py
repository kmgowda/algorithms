"""Volume 7, Chapter 5 - Disjoint Set Union (Union-Find): Friend Groups.

Run:  python3 ch05_examples.py
"""

from __future__ import annotations

from typing import Hashable


class UnionFind:
    """Each group is a tree; the root is the group's 'leader'.
    Path compression + union by size make every operation nearly O(1) (amortized O(alpha(n)))."""

    def __init__(self) -> None:
        self.parent: dict[Hashable, Hashable] = {}
        self.size: dict[Hashable, int] = {}
        self.groups = 0

    def add(self, x: Hashable) -> None:
        if x not in self.parent:
            self.parent[x] = x
            self.size[x] = 1
            self.groups += 1

    def find(self, x: Hashable) -> Hashable:
        """Follow parents to the root, then point every visited node straight at the root (path compression)."""
        self.add(x)
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, a: Hashable, b: Hashable) -> bool:
        """Join the groups of a and b; the smaller tree hangs under the larger (union by size).
        Returns False if they were already in the same group."""
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.groups -= 1
        return True

    def connected(self, a: Hashable, b: Hashable) -> bool:
        return self.find(a) == self.find(b)

    def group_size(self, x: Hashable) -> int:
        return self.size[self.find(x)]


class NaiveUnionFind:
    """No tricks: unions can build long chains, so find can take O(n)."""

    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.steps = 0

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.steps += 1
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> None:
        self.parent[self.find(a)] = self.find(b)


def friend_groups(friendships: list[tuple[str, str]], people: list[str]) -> list[list[str]]:
    """Beginner example: who ends up in the same friend circle?"""
    uf = UnionFind()
    for p in people:
        uf.add(p)
    for a, b in friendships:
        uf.union(a, b)
    circles: dict[Hashable, list[str]] = {}
    for p in people:
        circles.setdefault(uf.find(p), []).append(p)
    return sorted(sorted(c) for c in circles.values())


def redundant_cable(cables: list[tuple[int, int]]) -> tuple[int, int] | None:
    """Industry example (LeetCode 684): the first network cable that connects two already-connected computers
    (it creates a loop and can be removed)."""
    uf = UnionFind()
    for a, b in cables:
        if not uf.union(a, b):
            return a, b
    return None


def count_islands(grid: list[str]) -> int:
    """Practical example (LeetCode 200 with union-find): join neighbouring land cells; count the groups."""
    uf = UnionFind()
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == "#":
                uf.add((r, c))
                if r and grid[r - 1][c] == "#":
                    uf.union((r, c), (r - 1, c))
                if c and row[c - 1] == "#":
                    uf.union((r, c), (r, c - 1))
    return uf.groups


if __name__ == "__main__":
    people = ["Ana", "Ben", "Cy", "Dev", "Eve", "Fay"]
    print(friend_groups([("Ana", "Ben"), ("Cy", "Dev"), ("Ben", "Eve")], people))
    print("redundant cable:", redundant_cable([(1, 2), (2, 3), (3, 4), (1, 4), (1, 5)]))
    print("islands:", count_islands(["##..#", "#...#", "..#..", "....#"]))
    n = 2000
    naive = NaiveUnionFind(n)
    for i in range(n - 1):
        naive.union(i, i + 1)                     # builds one long chain
    naive.steps = 0
    for i in range(n):
        naive.find(0)
    smart = UnionFind()
    for i in range(n - 1):
        smart.union(i, i + 1)

    def depth(x: int) -> int:
        d = 0
        while smart.parent[x] != x:
            x, d = smart.parent[x], d + 1
        return d

    print("naive steps for 2000 finds:", naive.steps, "| deepest node with union by size:", max(depth(i) for i in range(n)))
