"""Volume 6, Chapter 9 - Other Balanced Trees: Treaps, Splay Trees, AA Trees.

Run:  python3 ch09_examples.py
"""

from __future__ import annotations

import random
from typing import Any, Iterator


def inorder(node) -> Iterator[Any]:
    if node is not None:
        yield from inorder(node.left)
        yield node.key
        yield from inorder(node.right)


def height(node) -> int:
    return -1 if node is None else 1 + max(height(node.left), height(node.right))


# ------------------------------------------------------------------ treap: BST by key + heap by random priority
class TreapNode:
    def __init__(self, key: Any, priority: float) -> None:
        self.key, self.priority = key, priority
        self.left: TreapNode | None = None
        self.right: TreapNode | None = None


def split(node: TreapNode | None, key: Any) -> tuple[TreapNode | None, TreapNode | None]:
    """Cut a treap into (keys < key, keys >= key)."""
    if node is None:
        return None, None
    if node.key < key:
        node.right, right = split(node.right, key)
        return node, right
    left, node.left = split(node.left, key)
    return left, node


def merge(a: TreapNode | None, b: TreapNode | None) -> TreapNode | None:
    """Join two treaps where every key in a < every key in b. The higher priority becomes the root."""
    if a is None or b is None:
        return a or b
    if a.priority > b.priority:
        a.right = merge(a.right, b)
        return a
    b.left = merge(a, b.left)
    return b


class Treap:
    """Random priorities make the tree's shape random no matter what order keys arrive in: expected O(log n)."""

    def __init__(self, seed: int = 0) -> None:
        self.root: TreapNode | None = None
        self.rng = random.Random(seed)

    def insert(self, key: Any) -> None:
        if self.contains(key):
            return
        left, right = split(self.root, key)
        self.root = merge(merge(left, TreapNode(key, self.rng.random())), right)

    def delete(self, key: Any) -> None:
        left, rest = split(self.root, key)
        _, right = split(rest, _Successor(key))              # drop exactly `key`
        self.root = merge(left, right)

    def contains(self, key: Any) -> bool:
        node = self.root
        while node is not None:
            if key == node.key:
                return True
            node = node.left if key < node.key else node.right
        return False


class _Successor:
    """A value just above `key` for splitting: compares greater than key and less than anything bigger."""

    def __init__(self, key: Any) -> None:
        self.key = key

    def __gt__(self, other: Any) -> bool:
        return other <= self.key

    def __lt__(self, other: Any) -> bool:
        return other > self.key


def check_treap(node: TreapNode | None, low: Any = None, high: Any = None) -> None:
    if node is None:
        return
    assert (low is None or node.key > low) and (high is None or node.key < high), "order broken"
    for child in (node.left, node.right):
        assert child is None or child.priority <= node.priority, "heap order broken"
    check_treap(node.left, low, node.key)
    check_treap(node.right, node.key, high)


# ------------------------------------------------------------------ splay tree: move every accessed key to the root
class SplayNode:
    def __init__(self, key: Any) -> None:
        self.key = key
        self.left: SplayNode | None = None
        self.right: SplayNode | None = None


def _rotate_right(x: SplayNode) -> SplayNode:
    y = x.left
    assert y is not None
    x.left, y.right = y.right, x
    return y


def _rotate_left(x: SplayNode) -> SplayNode:
    y = x.right
    assert y is not None
    x.right, y.left = y.left, x
    return y


def splay(node: SplayNode | None, key: Any) -> SplayNode | None:
    """Bring `key` (or the last node on its search path) to the root with zig-zig and zig-zag rotations."""
    if node is None or node.key == key:
        return node
    if key < node.key:
        if node.left is None:
            return node
        if key < node.left.key:                                  # zig-zig
            node.left.left = splay(node.left.left, key)
            node = _rotate_right(node)
        elif key > node.left.key:                                # zig-zag
            node.left.right = splay(node.left.right, key)
            if node.left.right is not None:
                node.left = _rotate_left(node.left)
        return node if node.left is None else _rotate_right(node)
    if node.right is None:
        return node
    if key > node.right.key:                                     # zag-zag
        node.right.right = splay(node.right.right, key)
        node = _rotate_left(node)
    elif key < node.right.key:                                   # zag-zig
        node.right.left = splay(node.right.left, key)
        if node.right.left is not None:
            node.right = _rotate_right(node.right)
    return node if node.right is None else _rotate_left(node)


class SplayTree:
    """No balance information at all. Amortized O(log n) per operation; recently used keys sit near the top."""

    def __init__(self) -> None:
        self.root: SplayNode | None = None

    def insert(self, key: Any) -> None:
        self.root = splay(self.root, key)
        if self.root is not None and self.root.key == key:
            return
        node = SplayNode(key)
        if self.root is not None:
            if key < self.root.key:
                node.left, node.right, self.root.left = self.root.left, self.root, None
            else:
                node.right, node.left, self.root.right = self.root.right, self.root, None
        self.root = node

    def contains(self, key: Any) -> bool:
        self.root = splay(self.root, key)
        return self.root is not None and self.root.key == key


# ------------------------------------------------------------------ AA tree: red-black rules simplified with levels
class AANode:
    def __init__(self, key: Any) -> None:
        self.key = key
        self.level = 1
        self.left: AANode | None = None
        self.right: AANode | None = None


def skew(t: AANode | None) -> AANode | None:
    """A left child on the same level is not allowed: rotate right."""
    if t is not None and t.left is not None and t.left.level == t.level:
        left = t.left
        t.left, left.right = left.right, t
        return left
    return t


def aa_split(t: AANode | None) -> AANode | None:
    """Two right children on the same level are not allowed: rotate left and raise the middle node."""
    if t is not None and t.right is not None and t.right.right is not None and t.right.right.level == t.level:
        right = t.right
        t.right, right.left = right.left, t
        right.level += 1
        return right
    return t


def aa_insert(t: AANode | None, key: Any) -> AANode:
    if t is None:
        return AANode(key)
    if key < t.key:
        t.left = aa_insert(t.left, key)
    elif key > t.key:
        t.right = aa_insert(t.right, key)
    else:
        return t
    result = aa_split(skew(t))
    assert result is not None
    return result


def check_aa(t: AANode | None) -> None:
    if t is None:
        return
    if t.left is None and t.right is None:
        assert t.level == 1, "leaves have level 1"
    assert t.left is None or t.left.level == t.level - 1, "left child must be one level down"
    assert t.right is None or t.right.level in (t.level, t.level - 1), "right child at most one level down"
    assert t.right is None or t.right.right is None or t.right.right.level < t.level, "no two right links on a level"
    check_aa(t.left)
    check_aa(t.right)


def recent_contacts(lookups: list[str]) -> str:
    """Industry example: a phone's contact cache - a splay tree keeps the most recently searched name at the root."""
    tree = SplayTree()
    for name in sorted(set(lookups)):
        tree.insert(name)
    for name in lookups:
        tree.contains(name)
    assert tree.root is not None
    return tree.root.key


if __name__ == "__main__":
    treap = Treap(seed=1)
    for k in range(1000):
        treap.insert(k)
    check_treap(treap.root)
    print("treap with 1000 sorted inserts -> height", height(treap.root))
    s = SplayTree()
    for k in range(1, 8):
        s.insert(k)
    s.contains(3)
    print("splay root after searching 3:", s.root.key, "| inorder:", list(inorder(s.root)))   # type: ignore[union-attr]
    aa = None
    for k in range(1000):
        aa = aa_insert(aa, k)
    check_aa(aa)
    print("AA tree with 1000 sorted inserts -> height", height(aa))
    print("most recent contact at the root:", recent_contacts(["Maya", "Leo", "Zoe", "Leo", "Ana"]))
