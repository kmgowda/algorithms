"""Volume 7, Chapter 11 - The Big Comparison: Heap vs. BST; Segment Tree vs. Fenwick Tree; Union-Find vs. Search.

Compact copies of the structures are repeated here so they can be raced in one file.

Run:  python3 ch11_examples.py
"""

from __future__ import annotations

import bisect
import heapq
import random
import timeit
from collections import deque


class Fenwick:
    def __init__(self, n: int) -> None:
        self.n, self.box = n, [0] * (n + 1)

    def add(self, i: int, d: int) -> None:
        i += 1
        while i <= self.n:
            self.box[i] += d
            i += i & -i

    def prefix(self, i: int) -> int:
        s = 0
        while i:
            s += self.box[i]
            i -= i & -i
        return s


class SegSum:
    """Iterative bottom-up segment tree for sums (2n slots)."""

    def __init__(self, values: list[int]) -> None:
        self.n = len(values)
        self.t = [0] * self.n + list(values)
        for i in range(self.n - 1, 0, -1):
            self.t[i] = self.t[2 * i] + self.t[2 * i + 1]

    def set(self, i: int, v: int) -> None:
        i += self.n
        self.t[i] = v
        while i > 1:
            i //= 2
            self.t[i] = self.t[2 * i] + self.t[2 * i + 1]

    def total(self, lo: int, hi: int) -> int:
        """Sum of values[lo:hi] (hi exclusive)."""
        s, lo, hi = 0, lo + self.n, hi + self.n
        while lo < hi:
            if lo & 1:
                s, lo = s + self.t[lo], lo + 1
            if hi & 1:
                hi -= 1
                s += self.t[hi]
            lo, hi = lo // 2, hi // 2
        return s


def race_priority(n: int, seed: int = 0) -> dict[str, float]:
    """Push n random values, then pop them all: heapq vs. a sorted list kept with insort (BST stand-in)."""
    rng = random.Random(seed)
    data = [rng.random() for _ in range(n)]

    def with_heap() -> None:
        h: list[float] = []
        for x in data:
            heapq.heappush(h, x)
        while h:
            heapq.heappop(h)

    def with_sorted_list() -> None:
        s: list[float] = []
        for x in data:
            bisect.insort(s, x)
        s.reverse()
        while s:
            s.pop()

    return {name: min(timeit.repeat(fn, number=1, repeat=3)) for name, fn in
            (("heap", with_heap), ("sorted list", with_sorted_list))}


def race_range_sums(n: int, ops: int, seed: int = 0) -> dict[str, float]:
    """Mixed point updates and range sums: Fenwick vs. segment tree vs. recomputing with a plain list."""
    rng = random.Random(seed)
    values = [rng.randint(0, 9) for _ in range(n)]
    plan = [(rng.random() < 0.5, rng.randrange(n), rng.randrange(n)) for _ in range(ops)]

    def fenwick() -> None:
        f, cur = Fenwick(n), list(values)
        for i, v in enumerate(values):
            f.add(i, v)
        for is_update, a, b in plan:
            if is_update:
                f.add(a, b % 10 - cur[a])
                cur[a] = b % 10
            else:
                lo, hi = min(a, b), max(a, b)
                f.prefix(hi + 1) - f.prefix(lo)

    def segment() -> None:
        s = SegSum(values)
        for is_update, a, b in plan:
            if is_update:
                s.set(a, b % 10)
            else:
                s.total(min(a, b), max(a, b) + 1)

    def plain() -> None:
        cur = list(values)
        for is_update, a, b in plan:
            if is_update:
                cur[a] = b % 10
            else:
                sum(cur[min(a, b):max(a, b) + 1])

    return {name: min(timeit.repeat(fn, number=1, repeat=3)) for name, fn in
            (("Fenwick", fenwick), ("segment tree", segment), ("plain list", plain))}


def connected_after_each_edge(n: int, edges: list[tuple[int, int]], a: int, b: int) -> tuple[list[bool], list[bool]]:
    """Answer 'are a and b connected?' after every new edge, two ways: union-find vs. a fresh BFS each time."""
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]               # path halving
            x = parent[x]
        return x

    uf_answers, bfs_answers, adj = [], [], [[] for _ in range(n)]
    for u, v in edges:
        parent[find(u)] = find(v)
        uf_answers.append(find(a) == find(b))
        adj[u].append(v)
        adj[v].append(u)
        seen, queue = {a}, deque([a])
        while queue:
            x = queue.popleft()
            for y in adj[x]:
                if y not in seen:
                    seen.add(y)
                    queue.append(y)
        bfs_answers.append(b in seen)
    return uf_answers, bfs_answers


def choose(question: str) -> str:
    """The chapter's decision table as code."""
    return {
        "next most urgent item": "binary heap",
        "most urgent, plus sorted iteration or search by key": "balanced BST",
        "range sums with point updates": "Fenwick tree",
        "range min/max with updates, or range updates": "segment tree",
        "range min/max on static data": "sparse table",
        "are these connected, as links are added": "union-find",
        "path between two points, or links removed": "BFS/DFS",
        "seen before, with tiny memory": "Bloom filter",
        "count distinct, with tiny memory": "HyperLogLog",
        "sorted map that many threads update": "skip list",
    }[question]


if __name__ == "__main__":
    print({k: round(v, 4) for k, v in race_priority(20_000).items()})
    print({k: round(v, 4) for k, v in race_range_sums(20_000, 5_000).items()})
    rng = random.Random(3)
    edges = [(rng.randrange(200), rng.randrange(200)) for _ in range(300)]
    uf, bfs = connected_after_each_edge(200, edges, 0, 1)
    print("union-find and BFS agree:", uf == bfs, "| first connected after edge", uf.index(True) + 1 if True in uf else None)
    print(choose("range sums with point updates"))
