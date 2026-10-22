"""Volume 3, Chapter 17 - Segment Trees.

Run:  python3 ch17_examples.py
"""

from __future__ import annotations

import random

DAYS = [3, 1, 4, 1, 5, 9, 2, 6]


class SegmentTree:
    """Range sums with point updates. Node 1 covers everything; node i has children 2i and 2i+1 (Figure 17.1)."""

    def __init__(self, values: list[int]):
        self.n = len(values)
        self.t = [0] * (4 * max(1, self.n))
        self.visited = 0
        if self.n:                                    # an empty list has nothing to build
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
        """Sum of values[a..b]: use whole nodes that fit inside the range (Figure 17.2)."""
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
        """Set values[i] and fix the totals on the path to the root (Figure 17.3). Returns nodes changed."""
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


class LazySegmentTree:
    """Range add and range sum. A node fully inside an added range keeps the change as a pending tag
    and passes it to its children only when a later operation must look inside (Section 17.7)."""

    def __init__(self, values: list[int]):
        self.n = len(values)
        self.t = [0] * (4 * max(1, self.n))
        self.pending = [0] * (4 * max(1, self.n))
        self.visited = 0
        if self.n:
            self._build(1, 0, self.n - 1, values)

    def _build(self, node, lo, hi, values):
        if lo == hi:
            self.t[node] = values[lo]
            return
        mid = (lo + hi) // 2
        self._build(2 * node, lo, mid, values)
        self._build(2 * node + 1, mid + 1, hi, values)
        self.t[node] = self.t[2 * node] + self.t[2 * node + 1]

    def _tag(self, node, lo, hi, d):
        self.t[node] += d * (hi - lo + 1)             # every day below gains d
        if lo < hi:
            self.pending[node] += d                   # ...but the children have not been told yet

    def _push_down(self, node, lo, hi):
        if self.pending[node]:
            mid = (lo + hi) // 2
            self._tag(2 * node, lo, mid, self.pending[node])
            self._tag(2 * node + 1, mid + 1, hi, self.pending[node])
            self.pending[node] = 0

    def range_add(self, a: int, b: int, d: int) -> list[tuple[int, int]]:
        """Add d to every value in a..b. Returns the (lo, hi) stretches that received a pending tag."""
        tagged = []
        self.visited = 0
        if self.n:
            self._add(1, 0, self.n - 1, a, b, d, tagged)
        return tagged

    def _add(self, node, lo, hi, a, b, d, tagged):
        self.visited += 1
        if b < lo or hi < a:
            return                                    # misses the range
        if a <= lo and hi <= b:
            self._tag(node, lo, hi, d)                # fully inside: tag it and stop
            tagged.append((lo, hi))
            return
        self._push_down(node, lo, hi)                 # partly inside: pass old tags on first
        mid = (lo + hi) // 2
        self._add(2 * node, lo, mid, a, b, d, tagged)
        self._add(2 * node + 1, mid + 1, hi, a, b, d, tagged)
        self.t[node] = self.t[2 * node] + self.t[2 * node + 1]

    def query(self, a: int, b: int) -> int:
        """Sum of values a..b, pushing tags down on the way into partly covered nodes."""
        self.visited = 0
        return self._query(1, 0, self.n - 1, a, b) if self.n else 0

    def _query(self, node, lo, hi, a, b):
        self.visited += 1
        if b < lo or hi < a:
            return 0
        if a <= lo and hi <= b:
            return self.t[node]
        self._push_down(node, lo, hi)
        mid = (lo + hi) // 2
        return self._query(2 * node, lo, mid, a, b) + self._query(2 * node + 1, mid + 1, hi, a, b)

    def tags(self) -> dict[tuple[int, int], int]:
        """Every (lo, hi) stretch that still holds a pending tag."""
        out = {}

        def walk(node, lo, hi):
            if self.pending[node]:
                out[(lo, hi)] = self.pending[node]
            if lo < hi:
                mid = (lo + hi) // 2
                walk(2 * node, lo, mid)
                walk(2 * node + 1, mid + 1, hi)
        if self.n:
            walk(1, 0, self.n - 1)
        return out

    def totals(self) -> dict[tuple[int, int], int]:
        """The stored total of every (lo, hi) stretch, as it is held right now."""
        out = {}

        def walk(node, lo, hi):
            out[(lo, hi)] = self.t[node]
            if lo < hi:
                mid = (lo + hi) // 2
                walk(2 * node, lo, mid)
                walk(2 * node + 1, mid + 1, hi)
        if self.n:
            walk(1, 0, self.n - 1)
        return out


def dashboard_day(days: int = 1000, queries: int = 5000, corrections: int = 2000, seed: int = 1):
    """Section 17.9: replay one day of mixed questions and corrections three ways.
    Returns the steps each approach takes; every answer is checked to agree."""
    rng = random.Random(seed)
    counts = [rng.randint(0, 50) for _ in range(days)]
    plain, tree = counts[:], SegmentTree(counts)
    prefix = [0]
    for c in counts:
        prefix.append(prefix[-1] + c)
    ops = ["q"] * queries + ["u"] * corrections
    rng.shuffle(ops)
    steps = {"prefix sums": 0, "plain array": 0, "segment tree": 0}
    for op in ops:
        if op == "q":
            a = rng.randrange(days)
            b = rng.randrange(a, days)
            ans_prefix = prefix[b + 1] - prefix[a]
            steps["prefix sums"] += 1
            ans_plain = sum(plain[a:b + 1])
            steps["plain array"] += b - a + 1
            ans_tree = tree.query(a, b)
            steps["segment tree"] += tree.visited
            assert ans_prefix == ans_plain == ans_tree
        else:
            i, v = rng.randrange(days), rng.randint(0, 50)
            plain[i] = v
            steps["plain array"] += 1
            steps["segment tree"] += len(tree.update(i, v))
            for j in range(i + 1, days + 1):
                prefix[j] = prefix[j - 1] + plain[j - 1]
            steps["prefix sums"] += days - i
    return steps


if __name__ == "__main__":
    st = SegmentTree(DAYS)
    print(st.t[1:16])
    print(st.query(1, 6), st.used_nodes(1, 6), st.visited)
    print(st.update(5, 4), st.t[1:16], st.query(1, 6))
    big = SegmentTree([random.Random(1).randint(0, 9) for _ in range(1_000_000)])
    big.query(123_456, 876_543)
    print("visited for a million days:", big.visited)
    lz = LazySegmentTree(DAYS)
    print(lz.range_add(2, 5, 1), lz.visited, lz.tags(), lz.t[1])
    print(lz.query(3, 4), lz.visited, lz.tags())
    print(dashboard_day())
