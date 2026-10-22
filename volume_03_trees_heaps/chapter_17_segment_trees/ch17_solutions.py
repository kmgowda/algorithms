"""Volume 3, Chapter 17 - Segment Trees: companion code for the Thinking Problems (Section 17.17).

Run:  python3 ch17_solutions.py
"""

from __future__ import annotations

from ch17_examples import LazySegmentTree


def largest_index(n: int) -> int:
    """Thinking Problem 1: the largest node number used by the recursive tree over n positions."""
    best = 0

    def walk(node, lo, hi):
        nonlocal best
        best = max(best, node)
        if lo < hi:
            mid = (lo + hi) // 2
            walk(2 * node, lo, mid)
            walk(2 * node + 1, mid + 1, hi)
    if n:
        walk(1, 0, n - 1)
    return best


def combine(left, right):
    """Join two summaries (total, best prefix, best suffix, best stretch) of neighbouring stretches."""
    lt, lp, ls, lb = left
    rt, rp, rs, rb = right
    return (lt + rt, max(lp, lt + rp), max(rs, rt + ls), max(lb, rb, ls + rp))


class BestStretchTree:
    """Thinking Problem 2: the largest total of any unbroken stretch of days inside a..b, with point updates.
    Each node keeps four numbers; query and update are O(log n)."""

    def __init__(self, values: list[int]):
        self.n = len(values)
        self.t = [None] * (4 * max(1, self.n))
        if self.n:
            self._build(1, 0, self.n - 1, values)

    def _build(self, node, lo, hi, values):
        if lo == hi:
            v = values[lo]
            self.t[node] = (v, v, v, v)
            return
        mid = (lo + hi) // 2
        self._build(2 * node, lo, mid, values)
        self._build(2 * node + 1, mid + 1, hi, values)
        self.t[node] = combine(self.t[2 * node], self.t[2 * node + 1])

    def update(self, i: int, value: int, node=1, lo=0, hi=None) -> None:
        hi = self.n - 1 if hi is None else hi
        if lo == hi:
            self.t[node] = (value, value, value, value)
            return
        mid = (lo + hi) // 2
        if i <= mid:
            self.update(i, value, 2 * node, lo, mid)
        else:
            self.update(i, value, 2 * node + 1, mid + 1, hi)
        self.t[node] = combine(self.t[2 * node], self.t[2 * node + 1])

    def best(self, a: int, b: int):
        """Largest total of a non-empty stretch inside a..b; None for an empty or backwards range."""
        if self.n == 0 or a > b:
            return None
        return self._query(1, 0, self.n - 1, max(a, 0), min(b, self.n - 1))[3]

    def _query(self, node, lo, hi, a, b):
        if a <= lo and hi <= b:
            return self.t[node]
        mid = (lo + hi) // 2
        if b <= mid:
            return self._query(2 * node, lo, mid, a, b)
        if a > mid:
            return self._query(2 * node + 1, mid + 1, hi, a, b)
        return combine(self._query(2 * node, lo, mid, a, b), self._query(2 * node + 1, mid + 1, hi, a, b))


class ForgetfulLazyTree(LazySegmentTree):
    """Thinking Problem 3: the bug. RangeAdd that does not recompute a split box from its children."""

    def _add(self, node, lo, hi, a, b, d, tagged):
        self.visited += 1
        if b < lo or hi < a:
            return
        if a <= lo and hi <= b:
            self._tag(node, lo, hi, d)
            tagged.append((lo, hi))
            return
        self._push_down(node, lo, hi)
        mid = (lo + hi) // 2
        self._add(2 * node, lo, mid, a, b, d, tagged)
        self._add(2 * node + 1, mid + 1, hi, a, b, d, tagged)
        # BUG: the line  self.t[node] = self.t[2 * node] + self.t[2 * node + 1]  is missing


if __name__ == "__main__":
    print([(n, largest_index(n)) for n in (5, 6, 10)])
    gains = [3, -4, 5, -1, 2, -6, 4, 1]
    t = BestStretchTree(gains)
    print(t.best(0, 7), t.best(1, 4), t.best(5, 5))
    bad = ForgetfulLazyTree([3, 1, 4, 1, 5, 9, 2, 6])
    bad.range_add(2, 5, 1)
    print(bad.query(0, 7), bad.query(0, 3), bad.query(2, 3))
