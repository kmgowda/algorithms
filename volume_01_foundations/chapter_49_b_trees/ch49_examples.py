"""Volume 1, Chapter 49 - B-Trees.

Run:  python3 ch49_examples.py
"""

from __future__ import annotations

import bisect
import math


class BNode:
    __slots__ = ("keys", "children")

    def __init__(self, keys=None, children=None):
        self.keys, self.children = keys or [], children or []

    @property
    def leaf(self) -> bool:
        return not self.children


class BTree:
    """A B-tree whose nodes hold at most max_keys keys (an odd number); full nodes split on the way down."""

    def __init__(self, max_keys: int = 3, keys=()):
        assert max_keys % 2 == 1 and max_keys >= 3
        self.max_keys = max_keys
        self.root = BNode()
        self.splits = 0
        for k in keys:
            self.insert(k)

    def search(self, key) -> tuple[bool, int]:
        """Returns (found, nodes visited): each visited node is one disk read (Figure 49.2)."""
        n, visits = self.root, 0
        while True:
            visits += 1
            i = bisect.bisect_left(n.keys, key)
            if i < len(n.keys) and n.keys[i] == key:
                return True, visits
            if n.leaf:
                return False, visits
            n = n.children[i]

    def _split_child(self, parent: BNode, i: int) -> None:
        """Move the middle key of parent.children[i] up into parent (Figure 49.3)."""
        child = parent.children[i]
        mid = len(child.keys) // 2
        right = BNode(child.keys[mid + 1:], child.children[mid + 1:])
        parent.keys.insert(i, child.keys[mid])
        parent.children.insert(i + 1, right)
        child.keys, child.children = child.keys[:mid], child.children[:mid + 1]
        self.splits += 1

    def insert(self, key) -> None:
        if self.search(key)[0]:
            return
        if len(self.root.keys) == self.max_keys:          # a full root splits: the tree grows taller
            self.root = BNode([], [self.root])
            self._split_child(self.root, 0)
        n = self.root
        while not n.leaf:
            i = bisect.bisect_left(n.keys, key)
            if len(n.children[i].keys) == self.max_keys:
                self._split_child(n, i)
                if key > n.keys[i]:
                    i += 1
            n = n.children[i]
        bisect.insort(n.keys, key)

    def height(self) -> int:
        h, n = 0, self.root
        while not n.leaf:
            h, n = h + 1, n.children[0]
        return h

    def levels(self) -> list[list[list]]:
        """Keys of every node, level by level (for drawing and testing)."""
        out, level = [], [self.root]
        while level:
            out.append([n.keys for n in level])
            level = [c for n in level for c in n.children]
        return out

    def inorder(self, n=None) -> list:
        n = n or self.root
        if n.leaf:
            return list(n.keys)
        out = []
        for i, k in enumerate(n.keys):
            out += self.inorder(n.children[i]) + [k]
        return out + self.inorder(n.children[-1])

    def leaves_same_depth(self) -> bool:
        depths = set()

        def walk(n, d):
            if n.leaf:
                depths.add(d)
            for c in n.children:
                walk(c, d + 1)
        walk(self.root, 0)
        return len(depths) == 1


if __name__ == "__main__":
    t = BTree(3)
    for k in [58, 25, 84, 12, 47, 70, 91, 31, 63]:
        t.insert(k)
        print(k, t.levels())
    print(t.search(63), t.splits)
    big = BTree(199, range(1_000_000))
    print(big.height(), big.search(765_432), math.log2(1_000_000))
