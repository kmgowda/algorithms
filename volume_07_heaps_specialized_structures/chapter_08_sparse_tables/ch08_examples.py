"""Volume 7, Chapter 8 - Sparse Tables and Range Minimum Queries.

table[k][i] = min of values[i .. i + 2^k - 1]. Any range is covered by two overlapping power-of-two blocks.

Run:  python3 ch08_examples.py
"""

from __future__ import annotations

from typing import Callable


class SparseTable:
    """Static data only. Build O(n log n); query O(1) for 'overlap-safe' operations (min, max, gcd)."""

    def __init__(self, values: list[float], combine: Callable[[float, float], float] = min) -> None:
        self.combine = combine
        n = len(values)
        self.log = [0] * (n + 1)
        for i in range(2, n + 1):
            self.log[i] = self.log[i // 2] + 1               # floor(log2 i)
        self.table = [list(values)]
        k = 1
        while (1 << k) <= n:
            prev, half = self.table[k - 1], 1 << (k - 1)
            self.table.append([combine(prev[i], prev[i + half]) for i in range(n - (1 << k) + 1)])
            k += 1

    def query(self, left: int, right: int) -> float:
        """Two blocks of length 2^k, one starting at left and one ending at right, cover [left, right].
        They may overlap - fine for min, because min(x, x) = x."""
        k = self.log[right - left + 1]
        return self.combine(self.table[k][left], self.table[k][right - (1 << k) + 1])


def lowest_temperature(readings: list[float], periods: list[tuple[int, int]]) -> list[float]:
    """Beginner example: coldest reading in each period of a recorded (unchanging) weather log."""
    st = SparseTable(readings, min)
    return [st.query(a, b) for a, b in periods]


def lca_by_rmq(parent: dict[str, str | None], queries: list[tuple[str, str]]) -> list[str]:
    """Industry example: lowest common ancestor via an Euler tour + range minimum on depths (O(1) per query).
    Used when one big tree (an org chart, a file system, a taxonomy) gets millions of LCA questions."""
    children: dict[str, list[str]] = {}
    root = None
    for node, p in parent.items():
        if p is None:
            root = node
        else:
            children.setdefault(p, []).append(node)
    euler, depth, first = [], [], {}
    stack = [(root, 0, iter(children.get(root, [])))]
    euler.append(root)
    depth.append(0)
    first[root] = 0
    while stack:
        node, d, kids = stack[-1]
        child = next(kids, None)
        if child is None:
            stack.pop()
            if stack:
                euler.append(stack[-1][0])
                depth.append(stack[-1][1])
            continue
        first[child] = len(euler)
        euler.append(child)
        depth.append(d + 1)
        stack.append((child, d + 1, iter(children.get(child, []))))
    st = SparseTable([(dep, i) for i, dep in enumerate(depth)], min)    # (depth, position) pairs
    out = []
    for a, b in queries:
        lo, hi = sorted((first[a], first[b]))
        out.append(euler[st.query(lo, hi)[1]])
    return out


if __name__ == "__main__":
    temps = [12, 9, 14, 7, 11, 15, 6, 10]
    st = SparseTable(temps)
    print("rows:", [len(r) for r in st.table], "| min of days 1..5:", st.query(1, 5))
    print(lowest_temperature(temps, [(0, 3), (4, 7), (2, 2)]))
    tree = {"CEO": None, "CTO": "CEO", "CFO": "CEO", "Dev": "CTO", "QA": "CTO", "Ana": "Dev", "Acct": "CFO"}
    print(lca_by_rmq(tree, [("Ana", "QA"), ("Ana", "Acct"), ("Dev", "Ana")]))
