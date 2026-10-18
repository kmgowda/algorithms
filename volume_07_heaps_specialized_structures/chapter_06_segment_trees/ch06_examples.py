"""Volume 7, Chapter 6 - Segment Trees: Range Questions Answered Fast.

Run:  python3 ch06_examples.py
"""

from __future__ import annotations

from typing import Callable


class SegmentTree:
    """Each node stores the answer (sum, min, max, ...) for one segment of the array.
    The root covers everything; children split their parent's segment in half.
    Point update and range query are O(log n). `combine` must be associative, with `identity` as its neutral value."""

    def __init__(self, values: list[float], combine: Callable[[float, float], float] = lambda a, b: a + b,
                 identity: float = 0) -> None:
        self.n = len(values)
        self.combine, self.identity = combine, identity
        self.tree = [identity] * (4 * max(1, self.n))
        if self.n:
            self._build(values, 1, 0, self.n - 1)

    def _build(self, values: list[float], node: int, lo: int, hi: int) -> None:
        if lo == hi:
            self.tree[node] = values[lo]
            return
        mid = (lo + hi) // 2
        self._build(values, 2 * node, lo, mid)
        self._build(values, 2 * node + 1, mid + 1, hi)
        self.tree[node] = self.combine(self.tree[2 * node], self.tree[2 * node + 1])

    def update(self, index: int, value: float) -> None:
        """Set values[index] = value, then fix every segment containing it (one root-to-leaf path)."""
        def go(node: int, lo: int, hi: int) -> None:
            if lo == hi:
                self.tree[node] = value
                return
            mid = (lo + hi) // 2
            if index <= mid:
                go(2 * node, lo, mid)
            else:
                go(2 * node + 1, mid + 1, hi)
            self.tree[node] = self.combine(self.tree[2 * node], self.tree[2 * node + 1])
        go(1, 0, self.n - 1)

    def query(self, left: int, right: int) -> float:
        """Combine values[left..right] (inclusive). Segments fully inside are used whole; outside are skipped."""
        def go(node: int, lo: int, hi: int) -> float:
            if right < lo or hi < left:
                return self.identity                      # no overlap
            if left <= lo and hi <= right:
                return self.tree[node]                    # complete overlap
            mid = (lo + hi) // 2
            return self.combine(go(2 * node, lo, mid), go(2 * node + 1, mid + 1, hi))
        return go(1, 0, self.n - 1)


class LazySumTree:
    """Range ADD and range SUM, both O(log n), using lazy propagation:
    a pending addition is stored at a node and pushed to its children only when needed."""

    def __init__(self, values: list[int]) -> None:
        self.n = len(values)
        self.sum = [0] * (4 * max(1, self.n))
        self.lazy = [0] * (4 * max(1, self.n))
        for i, v in enumerate(values):
            self.add(i, i, v)

    def _push(self, node: int, lo: int, hi: int) -> None:
        if self.lazy[node]:
            mid = (lo + hi) // 2
            for child, a, b in ((2 * node, lo, mid), (2 * node + 1, mid + 1, hi)):
                self.lazy[child] += self.lazy[node]
                self.sum[child] += self.lazy[node] * (b - a + 1)
            self.lazy[node] = 0

    def add(self, left: int, right: int, delta: int) -> None:
        def go(node: int, lo: int, hi: int) -> None:
            if right < lo or hi < left:
                return
            if left <= lo and hi <= right:
                self.sum[node] += delta * (hi - lo + 1)
                self.lazy[node] += delta                   # children will learn about it later
                return
            self._push(node, lo, hi)
            mid = (lo + hi) // 2
            go(2 * node, lo, mid)
            go(2 * node + 1, mid + 1, hi)
            self.sum[node] = self.sum[2 * node] + self.sum[2 * node + 1]
        go(1, 0, self.n - 1)

    def total(self, left: int, right: int) -> int:
        def go(node: int, lo: int, hi: int) -> int:
            if right < lo or hi < left:
                return 0
            if left <= lo and hi <= right:
                return self.sum[node]
            self._push(node, lo, hi)
            mid = (lo + hi) // 2
            return go(2 * node, lo, mid) + go(2 * node + 1, mid + 1, hi)
        return go(1, 0, self.n - 1)


def cheapest_flight_in_window(prices: list[int], changes: list[tuple[int, int]], window: tuple[int, int]) -> int:
    """Industry example: daily flight prices change; ask for the cheapest day in a date range (a MIN segment tree)."""
    st = SegmentTree(prices, combine=min, identity=float("inf"))
    for day, price in changes:
        st.update(day, price)
    return int(st.query(*window))


if __name__ == "__main__":
    sales = [5, 8, 6, 3, 2, 7, 2, 6]                    # daily sales at a fruit stall
    st = SegmentTree(sales)
    print("sales days 2..5:", st.query(2, 5))
    st.update(3, 10)
    print("after correcting day 3:", st.query(2, 5))
    print("cheapest flight days 1..4:", cheapest_flight_in_window([320, 280, 300, 410, 260, 290], [(4, 500), (2, 250)], (1, 4)))
    lazy = LazySumTree([0] * 10)
    lazy.add(2, 6, 5)                                    # 5 extra seats booked on days 2-6
    lazy.add(4, 9, 1)
    print("seats on days 3..5:", lazy.total(3, 5))
