"""Volume 2, Chapter 29 - Fenwick Trees (Binary Indexed Trees).

Run:  python3 ch29_examples.py
"""

from __future__ import annotations

DAYS = [3, 1, 4, 1, 5, 9, 2, 6]


def lowbit(i: int) -> int:
    """The lowest set bit of i: how many days box i is responsible for (Figure 29.1)."""
    return i & -i


class Fenwick:
    """Box i (1-based) stores the total of the lowbit(i) days ending at day i."""

    def __init__(self, values: list[int]):
        self.n = len(values)
        self.tree = [0] * (self.n + 1)
        for i, v in enumerate(values, 1):
            self.add(i, v)

    def add(self, i: int, delta: int) -> list[int]:
        """Add delta to day i: climb to every box responsible for it (Figure 29.3)."""
        touched = []
        while i <= self.n:
            self.tree[i] += delta
            touched.append(i)
            i += lowbit(i)
        return touched

    def prefix(self, i: int) -> tuple[int, list[int]]:
        """Total of days 1..i: hop down through boxes that tile the stretch (Figure 29.2)."""
        total, hops = 0, []
        while i > 0:
            total += self.tree[i]
            hops.append(i)
            i -= lowbit(i)
        return total, hops

    def range_sum(self, a: int, b: int) -> int:
        """Total of days a..b (1-based, inclusive), as two prefixes (Chapter 8)."""
        return self.prefix(b)[0] - self.prefix(a - 1)[0]


def ranks(scores: list[int], top: int = 100) -> list[int]:
    """Section 29.8: for each arrival, how many earlier scores were lower."""
    f = Fenwick([0] * top)
    out = []
    for s in scores:
        out.append(f.prefix(s - 1)[0])
        f.add(s, 1)
    return out


if __name__ == "__main__":
    print(ranks([72, 95, 41, 88, 60]), ranks([50, 20, 70, 30]))
    f = Fenwick(DAYS)
    print(f.tree[1:], [lowbit(i) for i in range(1, 9)])
    print(f.prefix(7), f.prefix(6), f.range_sum(2, 7))
    print(f.add(6, -5), f.tree[1:], f.range_sum(2, 7))
    for i in (5, 6, 7, 8, 12, 13):
        print(i, bin(i), lowbit(i))
