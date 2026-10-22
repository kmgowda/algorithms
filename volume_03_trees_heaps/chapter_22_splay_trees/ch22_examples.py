"""Volume 3, Chapter 22 - Splay Trees.

A binary search tree that moves every key it touches to the root by zig, zig-zig and zig-zag steps
(Figure 22.2). No balance information is stored; the potential-function analysis of Section 22.6 shows that
any sequence of m operations on at most n keys costs O(m log n) rotations.

Run:  python3 ch22_examples.py
"""

from __future__ import annotations

import math
import random


class Node:
    __slots__ = ("key", "left", "right", "parent")

    def __init__(self, key, parent=None):
        self.key, self.left, self.right, self.parent = key, None, None, parent


class SplayTree:
    """`rotations` counts every single rotation; `steps` logs the splay steps of every splay so far."""

    def __init__(self, keys=()):
        self.root = None
        self.rotations = 0
        self.steps = []
        for k in keys:
            self.insert(k)

    def _rotate(self, x):
        """Lift x above its parent p, a single rotation, keeping the parent links right."""
        p, g = x.parent, x.parent.parent
        if x is p.left:
            p.left, x.right = x.right, p
            if p.left:
                p.left.parent = p
        else:
            p.right, x.left = x.left, p
            if p.right:
                p.right.parent = p
        p.parent, x.parent = x, g
        if g is None:
            self.root = x
        elif g.left is p:
            g.left = x
        else:
            g.right = x
        self.rotations += 1

    def splay(self, x):
        while x.parent is not None:
            p, g = x.parent, x.parent.parent
            if g is None:                                  # zig: p is the root
                self._rotate(x)
                self.steps.append("zig")
            elif (x is p.left) == (p is g.left):           # zig-zig: rotate the grandparent first
                self._rotate(p)
                self._rotate(x)
                self.steps.append("zig-zig")
            else:                                          # zig-zag: rotate x twice
                self._rotate(x)
                self._rotate(x)
                self.steps.append("zig-zag")
        return x

    def search(self, key) -> bool:
        """Find key and splay its node; if key is missing, splay the last node visited (Section 22.5)."""
        n, last = self.root, None
        while n is not None and n.key != key:
            last = n
            n = n.left if key < n.key else n.right
        if n is not None or last is not None:
            self.splay(n if n is not None else last)
        return n is not None

    def insert(self, key) -> bool:
        """Insert as in a plain BST, then splay the new node. A duplicate is splayed and not added."""
        if self.root is None:
            self.root = Node(key)
            return True
        n = self.root
        while True:
            if key == n.key:
                self.splay(n)
                return False
            child = n.left if key < n.key else n.right
            if child is None:
                child = Node(key, n)
                if key < n.key:
                    n.left = child
                else:
                    n.right = child
                self.splay(child)
                return True
            n = child

    def delete(self, key) -> bool:
        if not self.search(key):                           # the key is now at the root, if present
            return False
        left, right = self.root.left, self.root.right
        if left is None:
            self.root = right
            if right:
                right.parent = None
            return True
        left.parent = None
        self.root = left
        m = left
        while m.right:
            m = m.right
        self.splay(m)                                      # the largest key on the left: no right child now
        m.right = right
        if right:
            right.parent = m
        return True

    # ---------------------------------------------------------------- inspection

    def find_node(self, key):
        n = self.root
        while n is not None and n.key != key:
            n = n.left if key < n.key else n.right
        return n

    def shape(self, n="root"):
        """(key, left, right) tuples, for drawing."""
        n = self.root if n == "root" else n
        return None if n is None else (n.key, self.shape(n.left), self.shape(n.right))

    def keys(self):
        out = []

        def walk(n):
            if n:
                walk(n.left)
                out.append(n.key)
                walk(n.right)
        walk(self.root)
        return out

    def height(self, n="root") -> int:
        n = self.root if n == "root" else n
        return -1 if n is None else 1 + max(self.height(n.left), self.height(n.right))

    def depth(self, key) -> int:
        d, n = 0, self.root
        while n.key != key:
            n = n.left if key < n.key else n.right
            d += 1
        return d

    def valid(self) -> bool:
        """Keys in BST order and every parent link consistent."""
        def ok(n, lo, hi, parent):
            if n is None:
                return True
            if n.parent is not parent or (lo is not None and n.key <= lo) or (hi is not None and n.key >= hi):
                return False
            return ok(n.left, lo, n.key, n) and ok(n.right, n.key, hi, n)
        return ok(self.root, None, None, None)

    def potential(self) -> float:
        """Phi = the sum over all nodes of rank(x) = log2 size(x) (Section 22.6)."""
        return sum(math.log2(s) for s in sizes(self.root).values())


def sizes(root) -> dict:
    """Subtree size of every node, without recursion (a long path would exceed Python's recursion limit)."""
    out, order, stack = {}, [], [root] if root else []
    while stack:
        n = stack.pop()
        order.append(n)
        stack.extend(c for c in (n.left, n.right) if c)
    for n in reversed(order):                              # children before parents
        out[n] = 1 + out.get(n.left, 0) + out.get(n.right, 0)
    return out


def size_of(n) -> int:
    return sizes(n).get(n, 0)


def access_lemma_slack(tree: SplayTree, key) -> float:
    """Splay the node holding key and return bound - amortized cost, where amortized cost = rotations + change
    in potential and bound = 3 (rank(root) - rank(x)) + 1. The access lemma says this is never negative."""
    x = tree.find_node(key)
    r_root, r_x = math.log2(size_of(tree.root)), math.log2(size_of(x))
    before, rot = tree.potential(), tree.rotations
    tree.splay(x)
    amortized = (tree.rotations - rot) + tree.potential() - before
    return 3 * (r_root - r_x) + 1 - amortized


def move_to_root(keys, key):
    """The naive rule: rotate the key up one level at a time (no zig-zig). Returns the tree's shape and height."""
    t = SplayTree()
    for k in keys:                                         # build a plain BST without splaying
        if t.root is None:
            t.root = Node(k)
            continue
        n = t.root
        while True:
            side = n.left if k < n.key else n.right
            if side is None:
                c = Node(k, n)
                if k < n.key:
                    n.left = c
                else:
                    n.right = c
                break
            n = side
    x = t.find_node(key)
    while x.parent is not None:
        t._rotate(x)
    return t.shape(), t.height(), t.rotations


def sorted_build(keys):
    """Insert keys in increasing order: each insert is one zig, and the tree becomes a left path."""
    return SplayTree(sorted(keys))


def sequential_cost(n: int) -> int:
    """Rotations to access 1, 2, ..., n in order after building the tree from 1..n in order."""
    t = SplayTree(range(1, n + 1))
    start = t.rotations
    for k in range(1, n + 1):
        t.search(k)
    return t.rotations - start


def random_workload(n: int, m: int, seed: int = 1, hot: float = 0.0):
    """Build from n shuffled keys, then make m searches; with hot > 0, that share of searches asks for one of
    10 popular keys. Returns (rotations per search, comparisons per search); a search that finds its key at
    depth d makes d + 1 comparisons."""
    rng = random.Random(seed)
    keys = list(range(n))
    rng.shuffle(keys)
    t = SplayTree(keys)
    popular = rng.sample(keys, 10)
    start, comparisons = t.rotations, 0
    for _ in range(m):
        k = rng.choice(popular) if rng.random() < hot else rng.randrange(n)
        comparisons += t.depth(k) + 1
        t.search(k)
    return (t.rotations - start) / m, comparisons / m


SHELF = [12, 25, 31, 47, 58, 63, 70, 84, 91]

if __name__ == "__main__":
    t = sorted_build(SHELF)
    print("sorted build:", t.shape(), "height", t.height())
    t.search(12)
    print("after search(12):", t.shape(), "height", t.height(), t.steps[-4:])
    print("move-to-root instead:", move_to_root(sorted(SHELF, reverse=True), 12)[1:])
    print("sequential access of 1000 keys:", sequential_cost(1000), "rotations")
    for hot in (0.0, 0.9):
        print(f"10,000 keys, hot share {hot}:", random_workload(10_000, 20_000, hot=hot), "rotations, comparisons")
