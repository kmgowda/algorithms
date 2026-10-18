"""Volume 6, Chapter 10 - B-Trees and B+ Trees: Trees for Disks and Databases.

A B-tree of minimum degree t: every node except the root holds between t-1 and 2t-1 keys (sorted);
an inner node with k keys has k+1 children; all leaves are at the same depth.

Run:  python3 ch10_examples.py
"""

from __future__ import annotations

import bisect
import math
from typing import Any


class BNode:
    def __init__(self, leaf: bool = True) -> None:
        self.keys: list[Any] = []
        self.children: list[BNode] = []
        self.leaf = leaf


class BTree:
    def __init__(self, t: int = 3) -> None:
        if t < 2:
            raise ValueError("minimum degree must be at least 2")
        self.t = t
        self.root = BNode()
        self.node_reads = 0                       # each node visit = one 'disk read' in a real database

    def search(self, key: Any) -> bool:
        node = self.root
        while True:
            self.node_reads += 1
            i = bisect.bisect_left(node.keys, key)    # binary search INSIDE the node
            if i < len(node.keys) and node.keys[i] == key:
                return True
            if node.leaf:
                return False
            node = node.children[i]

    def insert(self, key: Any) -> None:
        """Split full nodes on the way DOWN, so there is always room. The tree grows only at the root."""
        if self.search(key):
            return
        root = self.root
        if len(root.keys) == 2 * self.t - 1:
            new_root = BNode(leaf=False)
            new_root.children.append(root)
            self._split_child(new_root, 0)
            self.root = new_root
        self._insert_nonfull(self.root, key)

    def _split_child(self, parent: BNode, i: int) -> None:
        """A full child (2t-1 keys) becomes two children of t-1 keys; its middle key moves up into parent."""
        t, full = self.t, parent.children[i]
        right = BNode(leaf=full.leaf)
        middle = full.keys[t - 1]
        right.keys, full.keys = full.keys[t:], full.keys[:t - 1]
        if not full.leaf:
            right.children, full.children = full.children[t:], full.children[:t]
        parent.keys.insert(i, middle)
        parent.children.insert(i + 1, right)

    def _insert_nonfull(self, node: BNode, key: Any) -> None:
        while not node.leaf:
            i = bisect.bisect_left(node.keys, key)
            if len(node.children[i].keys) == 2 * self.t - 1:
                self._split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            node = node.children[i]
        bisect.insort(node.keys, key)

    def keys_in_order(self) -> list[Any]:
        out: list[Any] = []

        def walk(node: BNode) -> None:
            for i, k in enumerate(node.keys):
                if not node.leaf:
                    walk(node.children[i])
                out.append(k)
            if not node.leaf:
                walk(node.children[-1])

        walk(self.root)
        return out

    def height(self) -> int:
        h, node = 0, self.root
        while not node.leaf:
            node, h = node.children[0], h + 1
        return h


def check(tree: BTree) -> None:
    """Key counts within limits, keys sorted, children count = keys + 1, all leaves at one depth."""
    leaf_depths: set[int] = set()

    def visit(node: BNode, depth: int, low: Any, high: Any, is_root: bool) -> None:
        assert node.keys == sorted(node.keys), "keys not sorted"
        assert len(node.keys) <= 2 * tree.t - 1, "node too full"
        assert is_root or len(node.keys) >= tree.t - 1, "node too empty"
        assert all((low is None or k > low) and (high is None or k < high) for k in node.keys), "order broken"
        if node.leaf:
            leaf_depths.add(depth)
            return
        assert len(node.children) == len(node.keys) + 1, "wrong number of children"
        bounds = [low] + node.keys + [high]
        for i, child in enumerate(node.children):
            visit(child, depth + 1, bounds[i], bounds[i + 1], False)

    visit(tree.root, 0, None, None, True)
    assert len(leaf_depths) <= 1, "leaves at different depths"


class BPlusLeafChain:
    """B+ tree idea in miniature: all keys live in LEAVES, and leaves are linked left to right,
    so a range scan finds the first leaf once and then just follows links (like ORDER BY ... BETWEEN)."""

    def __init__(self, sorted_keys: list[Any], leaf_size: int = 4) -> None:
        self.leaves = [sorted_keys[i:i + leaf_size] for i in range(0, len(sorted_keys), leaf_size)]
        self.separators = [leaf[0] for leaf in self.leaves[1:]]      # what the inner levels would store

    def range(self, low: Any, high: Any) -> tuple[list[Any], int]:
        """Returns (keys in [low, high], leaves visited)."""
        i = bisect.bisect_right(self.separators, low)              # descend once
        out, visited = [], 0
        while i < len(self.leaves):
            visited += 1
            for k in self.leaves[i]:
                if k > high:
                    return out, visited
                if k >= low:
                    out.append(k)
            i += 1                                                 # follow the link to the next leaf
        return out, visited


def reads_for_billion(t: int) -> int:
    """Industry example: how many node reads to find one key among a billion with minimum degree t (worst case)?
    Height is at most floor(log_t((n + 1) / 2)); a search reads one node per level."""
    return math.floor(math.log((1e9 + 1) / 2, t)) + 1


if __name__ == "__main__":
    tree = BTree(t=3)
    for k in range(1, 101):
        tree.insert(k)
    check(tree)
    print("100 keys, t=3 -> height", tree.height(), "| root keys:", tree.root.keys)
    tree.node_reads = 0
    tree.search(77)
    print("node reads to find 77:", tree.node_reads)
    chain = BPlusLeafChain(list(range(0, 200, 5)))
    print("range 42..80 ->", chain.range(42, 80))
    print("worst-case reads among a billion keys, t=500:", reads_for_billion(500))
