"""Volume 1, Chapter 57 - Segment Trees.

Run:  python3 ch57_examples.py
"""

from __future__ import annotations

import random

DAYS = [3, 1, 4, 1, 5, 9, 2, 6]


class SegmentTree:
    """Range sums with point updates. Node 1 covers everything; node i has children 2i and 2i+1 (Figure 57.1)."""

    def __init__(self, values: list[int]):
        self.n = len(values)
        self.t = [0] * (4 * max(1, self.n))
        self.visited = 0
        self._build(1, 0, self.n - 1, values)

    def _build(self, node, lo, hi, values):
        if lo == hi:
            self.t[node] = values[lo]
            return
        mid = (lo + hi) // 2
        self._build(2 * node, lo, mid, values)
        self._build(2 * node + 1, mid + 1, hi, values)
        self.t[node] = self.t[2 * node] + self.t[2 * node + 1]

    def query(self, a: int, b: int) -> int:
        """Sum of values[a..b]: use whole nodes that fit inside the range (Figure 57.2)."""
        self.visited = 0
        return self._query(1, 0, self.n - 1, a, b)

    def _query(self, node, lo, hi, a, b):
        self.visited += 1
        if b < lo or hi < a:
            return 0                                  # no overlap
        if a <= lo and hi <= b:
            return self.t[node]                       # fully inside: use the stored total
        mid = (lo + hi) // 2
        return self._query(2 * node, lo, mid, a, b) + self._query(2 * node + 1, mid + 1, hi, a, b)

    def update(self, i: int, value: int) -> list[int]:
        """Set values[i] and fix the totals on the path to the root (Figure 57.3). Returns nodes changed."""
        path = []
        node, lo, hi = 1, 0, self.n - 1
        while lo != hi:
            path.append(node)
            mid = (lo + hi) // 2
            node, lo, hi = (2 * node, lo, mid) if i <= mid else (2 * node + 1, mid + 1, hi)
        self.t[node] = value
        path.append(node)
        for p in reversed(path[:-1]):
            self.t[p] = self.t[2 * p] + self.t[2 * p + 1]
        return path

    def used_nodes(self, a: int, b: int) -> list[tuple[int, int]]:
        """The (lo, hi) ranges of the stored totals that a query adds together."""
        out = []

        def walk(node, lo, hi):
            if b < lo or hi < a:
                return
            if a <= lo and hi <= b:
                out.append((lo, hi))
                return
            mid = (lo + hi) // 2
            walk(2 * node, lo, mid)
            walk(2 * node + 1, mid + 1, hi)
        walk(1, 0, self.n - 1)
        return out


if __name__ == "__main__":
    st = SegmentTree(DAYS)
    print(st.t[1:16])
    print(st.query(1, 6), st.used_nodes(1, 6), st.visited)
    print(st.update(5, 4), st.t[1:16], st.query(1, 6))
    big = SegmentTree([random.Random(1).randint(0, 9) for _ in range(1_000_000)])
    big.query(123_456, 876_543)
    print("visited for a million days:", big.visited)
