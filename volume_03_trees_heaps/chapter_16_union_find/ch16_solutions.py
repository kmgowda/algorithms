"""Volume 3, Chapter 16 - Union-Find: companion code for the Thinking Problems (Section 16.17).

Run:  python3 ch16_solutions.py
"""

from __future__ import annotations


def tallest(parent: dict) -> int:
    """The greatest number of steps from any item to its root."""
    best = 0
    for x in parent:
        d = 0
        while parent[x] != x:
            x, d = parent[x], d + 1
        best = max(best, d)
    return best


class RollbackUnionFind:
    """Thinking Problem 2: union by size WITHOUT path compression, plus undo of the latest union.
    find is O(log n); union is O(log n); undo is O(1), because a union changes only two fields."""

    def __init__(self, items):
        self.parent = {x: x for x in items}
        self.size = {x: 1 for x in items}
        self.groups = len(self.parent)
        self.history: list = []                     # (child root, parent root), or None for a redundant union

    def find(self, x):
        while self.parent[x] != x:
            x = self.parent[x]
        return x

    def union(self, a, b) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            self.history.append(None)
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.groups -= 1
        self.history.append((rb, ra))
        return True

    def undo(self) -> bool:
        """Cancel the latest union not yet undone. Returns False when there is nothing to undo."""
        if not self.history:
            return False
        last = self.history.pop()
        if last is not None:
            rb, ra = last
            self.parent[rb] = rb
            self.size[ra] -= self.size[rb]
            self.groups += 1
        return True


class StaleSizeUnionFind:
    """Thinking Problem 3: the bug. Union by size that compares the sizes stored at a and b, not at their roots."""

    def __init__(self, items):
        self.parent = {x: x for x in items}
        self.size = {x: 1 for x in items}

    def find(self, x):
        while self.parent[x] != x:
            x = self.parent[x]
        return x

    def union(self, a, b) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[a] < self.size[b]:             # BUG: should be size[ra] < size[rb]
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True


if __name__ == "__main__":
    from ch16_examples import UnionByRank, UnionFind
    unions = [(0, 1), (0, 2), (0, 3), (0, 4), (5, 6), (7, 8), (5, 7), (0, 5)]
    by_size, by_rank = UnionFind(range(9)), UnionByRank(range(9))
    for a, b in unions:
        by_size.union(a, b)
        by_rank.union(a, b)
    print("size:", tallest(by_size.parent), by_size.find(8), " rank:", tallest(by_rank.parent), by_rank.find(8))
    bug = StaleSizeUnionFind(range(8))
    for i in range(1, 8):
        bug.union(i, 0)
    print("stale sizes, depth:", tallest(bug.parent))
