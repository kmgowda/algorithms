"""Volume 3, Chapter 22 - Splay Trees: companion code for the Thinking Problems (Section 22.16).

Run:  python3 ch22_solutions.py
"""

from __future__ import annotations

from ch22_examples import Node, SplayTree


def path_splay_height(n: int) -> int:
    """Thinking Problem 1: build the left path n, n-1, ..., 1 (insert 1..n in order) and splay 1."""
    t = SplayTree(range(1, n + 1))
    t.search(1)
    return t.height()


def split(tree: SplayTree, key):
    """Split into (keys < key, keys >= key), two splay trees, by one splay (Thinking Problem 2)."""
    small, large = SplayTree(), SplayTree()
    tree.search(key)                       # the key, or a neighbour of where it would be, is now the root
    r = tree.root
    if r is None:
        return small, large
    if r.key < key:
        small.root, large.root = r, r.right
        r.right = None
    else:
        small.root, large.root = r.left, r
        r.left = None
    for t in (small, large):
        if t.root:
            t.root.parent = None
    tree.root = None
    return small, large


def join(small: SplayTree, large: SplayTree) -> SplayTree:
    """Every key of small is below every key of large: splay small's maximum and hang large on its right."""
    if small.root is None:
        return large
    m = small.root
    while m.right:
        m = m.right
    small.splay(m)
    m.right = large.root
    if large.root:
        large.root.parent = m
    small.rotations += large.rotations
    return small


def delete_range(tree: SplayTree, a, b):
    """Remove every key k with a <= k <= b in O(log n) amortized time; return (new tree, keys removed)."""
    if a > b:
        return tree, 0
    left, rest = split(tree, a)
    middle, right = split_after(rest, b)
    return join(left, right), len(middle.keys())


def split_after(tree: SplayTree, key):
    """Split into (keys <= key, keys > key)."""
    small, large = SplayTree(), SplayTree()
    tree.search(key)
    r = tree.root
    if r is None:
        return small, large
    if r.key <= key:
        small.root, large.root = r, r.right
        r.right = None
    else:
        small.root, large.root = r.left, r
        r.left = None
    for t in (small, large):
        if t.root:
            t.root.parent = None
    tree.root = None
    return small, large


class MoveToRootTree(SplayTree):
    """Thinking Problem 3: the tempting simplification, rotating x with its parent until it is the root."""

    def splay(self, x):
        while x.parent is not None:
            self._rotate(x)
            self.steps.append("single")
        return x


def sequential_after_path(cls, n: int, rounds: int = 1) -> int:
    """Build the path from 1..n in order with cls's own rule, then access 1, 2, ..., n `rounds` times."""
    t = cls(range(1, n + 1))
    start = t.rotations
    for _ in range(rounds):
        for k in range(1, n + 1):
            t.search(k)
    return t.rotations - start


if __name__ == "__main__":
    print([path_splay_height(n) for n in range(1, 13)])
    t = SplayTree([12, 25, 31, 47, 58, 63, 70, 84, 91])
    t, gone = delete_range(t, 30, 65)
    print("delete 30..65:", gone, t.keys())
    for n in (5, 100, 1000):
        print(n, sequential_after_path(MoveToRootTree, n, 2), sequential_after_path(SplayTree, n, 2))
