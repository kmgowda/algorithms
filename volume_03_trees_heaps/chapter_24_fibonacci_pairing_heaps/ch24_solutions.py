"""Volume 3, Chapter 24 - Fibonacci and Pairing Heaps: companion code for the Thinking Problems (Section 24.18).

Run:  python3 ch24_solutions.py
"""

from __future__ import annotations

from ch24_examples import FibHeap, degree_bound, fib


def is_binomial_forest(heap: FibHeap) -> bool:
    """Thinking Problem 1: every tree is a binomial tree B_d (children of degrees 0, 1, ..., d - 1, so
    exactly 2**d nodes)."""
    def check(x):
        degrees = sorted(c.degree for c in x.children)
        if degrees != list(range(x.degree)):
            return None
        sizes = [check(c) for c in x.children]
        if None in sizes:
            return None
        return 1 + sum(sizes)
    for r in heap.roots:
        size = check(r)
        if size is None or size != 2 ** r.degree:
            return False
    return True


def report_at_most(heap: FibHeap, bound):
    """Thinking Problem 2: every (key, item) with key <= bound, without removing anything.
    Consolidate first (amortized O(log n)), then walk down from the roots, stopping at keys above the bound:
    by heap order, nothing below them can qualify. Returns (entries, nodes visited)."""
    heap.consolidate()
    found, visited = [], 0
    stack = list(heap.roots)
    while stack:
        x = stack.pop()
        visited += 1
        if x.key <= bound:
            found.append((x.key, x.item))
            stack.extend(x.children)
    return found, visited


class NoCascadeFibHeap(FibHeap):
    """Thinking Problem 3: the 'simplification' that cuts a node but never marks or cascades."""

    def _cascade(self, y):
        return


def star(cls, d: int):
    """Insert 0..2**d, delete-min (leaving one binomial tree B_d rooted at 1), then delete every node at depth
    two or more, deepest first. Returns (degree of the root holding 1, its size, items left, the heap)."""
    h = cls()
    nodes = [h.insert(k) for k in range(2 ** d + 1)]
    h.delete_min()
    root = nodes[1]
    deep = []

    def collect(x, depth):
        for c in list(x.children):
            collect(c, depth + 1)
        if depth >= 2:
            deep.append(x)
    collect(root, 0)
    for x in deep:
        h.delete(x)
    holder = root
    while holder.parent is not None:
        holder = holder.parent
    size = sum(1 for _ in _subtree(holder))
    return holder.degree, size, len(h), h


def _subtree(x):
    yield x
    for c in x.children:
        yield from _subtree(c)


if __name__ == "__main__":
    h = FibHeap(range(9))
    h.delete_min()
    print("binomial after insert/delete-min only:", is_binomial_forest(h))
    print("report <= 4:", sorted(report_at_most(h, 4)[0]))
    for cls in (NoCascadeFibHeap, FibHeap):
        deg, size, n, heap = star(cls, 4)
        print(cls.__name__, "root degree", deg, "size", size, "items", n, "F(d+2) =", fib(deg + 2),
              "valid:", heap.valid(), "D(n) =", degree_bound(n))
