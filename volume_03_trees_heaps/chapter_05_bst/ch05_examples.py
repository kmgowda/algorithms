"""Volume 3, Chapter 5 - Binary Search Trees.

Run:  python3 ch05_examples.py
"""

from __future__ import annotations

import random

ORDER = [58, 25, 84, 12, 47, 70, 91, 31, 63]


class _Node:
    __slots__ = ("key", "left", "right")

    def __init__(self, key):
        self.key, self.left, self.right = key, None, None


class BST:
    """Smaller keys to the left, larger to the right (Figures 5.1 to 5.4). Duplicates are ignored."""

    def __init__(self, keys=()):
        self.root = None
        for k in keys:
            self.insert(k)

    def search_path(self, key) -> list:
        path, n = [], self.root
        while n is not None:
            path.append(n.key)
            if key == n.key:
                break
            n = n.left if key < n.key else n.right
        return path

    def contains(self, key) -> bool:
        p = self.search_path(key)
        return bool(p) and p[-1] == key

    def insert(self, key) -> None:
        if self.root is None:
            self.root = _Node(key)
            return
        n = self.root
        while True:
            if key == n.key:
                return
            side = "left" if key < n.key else "right"
            nxt = getattr(n, side)
            if nxt is None:
                setattr(n, side, _Node(key))
                return
            n = nxt

    def delete(self, key, use_predecessor: bool = False) -> None:
        """Three cases (Figure 5.4). A node with two children takes its successor's key, or its predecessor's."""
        self.root = self._delete(self.root, key, use_predecessor)

    def _delete(self, n, key, pred=False):
        if n is None:
            return None
        if key < n.key:
            n.left = self._delete(n.left, key, pred)
        elif key > n.key:
            n.right = self._delete(n.right, key, pred)
        else:
            if n.left is None:
                return n.right                     # leaf or one child
            if n.right is None:
                return n.left
            if pred:                               # two children: predecessor, the largest key on the left
                s = n.left
                while s.right is not None:
                    s = s.right
                n.key = s.key
                n.left = self._delete(n.left, s.key, pred)
            else:                                  # two children: successor, the smallest key on the right
                s = n.right
                while s.left is not None:
                    s = s.left
                n.key = s.key
                n.right = self._delete(n.right, s.key, pred)
        return n

    def floor(self, key):
        """The largest key <= key, or None (Figure 5.2): remember the last node where the walk went right."""
        best, n = None, self.root
        while n is not None:
            if key == n.key:
                return n.key
            if key < n.key:
                n = n.left
            else:
                best, n = n.key, n.right
        return best

    def ceiling(self, key):
        """The smallest key >= key, or None: remember the last node where the walk went left."""
        best, n = None, self.root
        while n is not None:
            if key == n.key:
                return n.key
            if key > n.key:
                n = n.right
            else:
                best, n = n.key, n.left
        return best

    def successor(self, key):
        """The next larger key after key, or None: the ceiling of anything just above key."""
        best, n = None, self.root
        while n is not None:
            if key < n.key:
                best, n = n.key, n.left
            else:
                n = n.right
        return best

    def lowest_common_ancestor(self, a, b):
        """Section 5.4: walk down while a and b lie on the same side; the first split point is the answer.
        Returns None if either key is missing."""
        if not (self.contains(a) and self.contains(b)):
            return None
        n = self.root
        while True:
            if a < n.key and b < n.key:
                n = n.left
            elif a > n.key and b > n.key:
                n = n.right
            else:
                return n.key

    def inorder(self) -> list:
        out = []

        def walk(n):
            if n:
                walk(n.left); out.append(n.key); walk(n.right)
        walk(self.root)
        return out

    def range(self, lo, hi) -> list:
        out = []

        def walk(n):
            if n is None:
                return
            if lo < n.key:
                walk(n.left)
            if lo <= n.key <= hi:
                out.append(n.key)
            if n.key < hi:
                walk(n.right)
        walk(self.root)
        return out

    def height(self) -> int:
        """Iterative, so that degenerate trees thousands of levels deep do not overflow the call stack."""
        best, stack = -1, [(self.root, 0)] if self.root else []
        while stack:
            n, d = stack.pop()
            best = max(best, d)
            for c in (n.left, n.right):
                if c:
                    stack.append((c, d + 1))
        return best

    def average_depth(self) -> float:
        total, count, stack = 0, 0, [(self.root, 0)] if self.root else []
        while stack:
            n, d = stack.pop()
            total += d
            count += 1
            for c in (n.left, n.right):
                if c:
                    stack.append((c, d + 1))
        return total / count


if __name__ == "__main__":
    t = BST(ORDER)
    print(t.search_path(63), t.search_path(47), t.search_path(65), t.inorder(), t.range(30, 70))
    t.insert(40)
    print(t.search_path(40))
    for k in (12, 70, 25):
        t.delete(k)
    print(t.inorder(), t.root.left.key)
    t = BST(ORDER)
    print(t.floor(60), t.ceiling(60), t.floor(10), t.ceiling(95), t.lowest_common_ancestor(31, 12),
          t.lowest_common_ancestor(31, 63))
    rng = random.Random(1)
    keys = rng.sample(range(1_000_000), 10_000)
    r = BST(keys)
    print(round(r.average_depth(), 1), r.height())
