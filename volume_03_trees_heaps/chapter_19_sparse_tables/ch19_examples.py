"""Volume 3, Chapter 19 - Sparse Tables.

Run:  python3 ch19_examples.py
"""

from __future__ import annotations

NOISE = [5, 3, 7, 4, 6, 2, 8, 9]


class SparseTable:
    """table[k][i] = minimum of the 2^k values starting at i (Figure 19.1). Built once; values never change."""

    def __init__(self, values: list[int]):
        self.table = [list(values)]
        k = 1
        while (1 << k) <= len(values):
            prev, half = self.table[-1], 1 << (k - 1)
            self.table.append([min(prev[i], prev[i + half]) for i in range(len(values) - (1 << k) + 1)])
            k += 1

    def query(self, a: int, b: int) -> tuple[int, tuple, tuple]:
        """Minimum of values[a..b]: two overlapping power-of-two windows (Figure 19.2). O(1)."""
        if not 0 <= a <= b < len(self.table[0]):      # a backwards range would read windows outside a..b
            raise IndexError("need 0 <= a <= b < number of values")
        k = (b - a + 1).bit_length() - 1          # largest power of two that fits
        left, right = (a, a + (1 << k) - 1), (b - (1 << k) + 1, b)
        return min(self.table[k][a], self.table[k][b - (1 << k) + 1]), left, right

    def cells(self) -> int:
        return sum(len(row) for row in self.table)


SECTIONS = {"Library": ["Fiction", "Science", "History"], "Fiction": ["Mystery", "Fantasy"],
            "Science": ["Physics", "Biology", "Maths"], "History": ["Ancient"], "Maths": ["Algebra", "Geometry"]}  # Chapter 1


class LCA:
    """Lowest common ancestor in O(1) per question: walk the tree once (an Euler tour, writing a node every time
    the walk is at it), then the shallowest node between two nodes' first visits is their meeting point."""

    def __init__(self, children: dict, root):
        self.tour, self.depth, self.first = [], [], {}
        stack = [(root, 0, 0)]
        while stack:
            node, d, k = stack.pop()
            self.first.setdefault(node, len(self.tour))
            self.tour.append(node)
            self.depth.append(d)
            kids = children.get(node, [])
            if k < len(kids):
                stack.append((node, d, k + 1))           # come back to node after this child
                stack.append((kids[k], d + 1, 0))
        self.rmq = SparseTable([(d, i) for i, d in enumerate(self.depth)])

    def query(self, u, v):
        a, b = sorted((self.first[u], self.first[v]))
        (_, i), _, _ = self.rmq.query(a, b)
        return self.tour[i]


if __name__ == "__main__":
    st = SparseTable(NOISE)
    for row in st.table:
        print(row)
    print(st.query(1, 6), st.query(2, 4), st.query(0, 7), st.cells())
    big = SparseTable(list(range(1_000_000)))
    print(len(big.table), big.cells())
    lca = LCA(SECTIONS, "Library")
    print(len(lca.tour), lca.query("Algebra", "Physics"), lca.query("Mystery", "Geometry"))
