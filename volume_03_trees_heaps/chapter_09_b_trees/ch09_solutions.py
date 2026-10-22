"""Volume 3, Chapter 9 - B-Trees: companion code for the Thinking Problems (Section 9.17).

Run:  python3 ch09_solutions.py
"""

from __future__ import annotations

import bisect

from ch09_examples import BTree


def off_spine_sizes(tree: BTree) -> set:
    """Thinking Problem 1: the key counts of every node that is not on the rightmost path."""
    sizes = set()

    def walk(n, on_spine):
        if not on_spine:
            sizes.add(len(n.keys))
        for i, c in enumerate(n.children):
            walk(c, on_spine and i == len(n.children) - 1)
    walk(tree.root, True)
    return sizes


def range_keys(tree: BTree, a, b) -> tuple[list, int]:
    """Thinking Problem 2: every key k with a <= k <= b, in order, and the number of nodes read.
    Reads at most 2(h + 1) + k / (t - 1) nodes for k keys reported."""
    out, reads = [], 0

    def visit(n):
        nonlocal reads
        reads += 1
        i = bisect.bisect_left(n.keys, a)          # the first key >= a; child i may hold keys >= a too
        while True:
            if not n.leaf:
                visit(n.children[i])               # keys between n.keys[i - 1] and n.keys[i]
            if i == len(n.keys) or n.keys[i] > b:
                return
            out.append(n.keys[i])
            i += 1
    if a <= b:
        visit(tree.root)
    return out, reads


if __name__ == "__main__":
    for mk in (3, 5, 7):
        print(mk, off_spine_sizes(BTree(mk, range(1, 501))))
    t = BTree(3, [58, 25, 84, 12, 47, 70, 91, 31, 63])
    print(range_keys(t, 30, 65))
    big = BTree(199, range(1_000_000))
    print([(k, range_keys(big, 500_000, 500_000 + k - 1)[1]) for k in (1, 100, 1000, 10_000)])
