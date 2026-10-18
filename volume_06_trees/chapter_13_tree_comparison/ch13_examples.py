"""Volume 6, Chapter 13 - The Big Comparison: BST vs. AVL vs. Red-Black vs. B-Tree vs. Hash Table.

Compact implementations are repeated here so they can be raced in one file.

Run:  python3 ch13_examples.py
"""

from __future__ import annotations

import bisect
import math
import random
import timeit
from typing import Any


class _N:
    __slots__ = ("key", "left", "right", "height")

    def __init__(self, key: Any) -> None:
        self.key, self.left, self.right, self.height = key, None, None, 0


def _h(n: _N | None) -> int:
    return -1 if n is None else n.height


def _fix(n: _N) -> None:
    n.height = 1 + max(_h(n.left), _h(n.right))


def _rot_right(y: _N) -> _N:
    x = y.left
    y.left, x.right = x.right, y
    _fix(y)
    _fix(x)
    return x


def _rot_left(x: _N) -> _N:
    y = x.right
    x.right, y.left = y.left, x
    _fix(x)
    _fix(y)
    return y


def avl_insert(n: _N | None, key: Any) -> _N:
    if n is None:
        return _N(key)
    if key < n.key:
        n.left = avl_insert(n.left, key)
    elif key > n.key:
        n.right = avl_insert(n.right, key)
    else:
        return n
    _fix(n)
    bf = _h(n.left) - _h(n.right)
    if bf > 1:
        if _h(n.left.left) < _h(n.left.right):
            n.left = _rot_left(n.left)
        return _rot_right(n)
    if bf < -1:
        if _h(n.right.right) < _h(n.right.left):
            n.right = _rot_right(n.right)
        return _rot_left(n)
    return n


def bst_insert(root: _N | None, key: Any) -> _N:
    """Plain, unbalanced BST insert (iterative)."""
    if root is None:
        return _N(key)
    node = root
    while True:
        side = "left" if key < node.key else "right"
        child = getattr(node, side)
        if child is None:
            setattr(node, side, _N(key))
            return root
        node = child


def height(root: _N | None) -> int:
    h, level = -1, [root] if root else []
    while level:
        h += 1
        level = [c for n in level for c in (n.left, n.right) if c]
    return h


def contains(root: _N | None, key: Any) -> bool:
    while root is not None:
        if key == root.key:
            return True
        root = root.left if key < root.key else root.right
    return False


def height_table(n: int, seed: int = 0) -> dict[str, dict[str, float]]:
    """Heights for sorted and random insertion orders, plus the theoretical bounds for red-black and B-trees."""
    keys = list(range(n))
    shuffled = keys[:]
    random.Random(seed).shuffle(shuffled)
    table: dict[str, dict[str, float]] = {}
    for name, insert in (("plain BST", bst_insert), ("AVL", avl_insert)):
        row = {}
        for order, data in (("sorted", keys), ("random", shuffled)):
            root = None
            for k in data:
                root = insert(root, k)
            row[order] = height(root)
        table[name] = row
    table["red-black bound"] = {"sorted": round(2 * math.log2(n + 1), 1), "random": round(2 * math.log2(n + 1), 1)}
    table["B-tree t=100 bound"] = {"sorted": math.floor(math.log((n + 1) / 2, 100)),
                                   "random": math.floor(math.log((n + 1) / 2, 100))}
    return table


def lookup_race(n: int, lookups: int = 2000, seed: int = 1) -> dict[str, float]:
    """Seconds for `lookups` membership tests: AVL tree vs. sorted list + bisect vs. Python set (hash table)."""
    rng = random.Random(seed)
    keys = rng.sample(range(10 * n), n)
    root = None
    for k in keys:
        root = avl_insert(root, k)
    sorted_keys = sorted(keys)
    as_set = set(keys)
    queries = [rng.randrange(10 * n) for _ in range(lookups)]

    def in_sorted(q: int) -> bool:
        i = bisect.bisect_left(sorted_keys, q)
        return i < len(sorted_keys) and sorted_keys[i] == q

    return {
        "AVL tree": min(timeit.repeat(lambda: [contains(root, q) for q in queries], number=1, repeat=3)),
        "sorted list + bisect": min(timeit.repeat(lambda: [in_sorted(q) for q in queries], number=1, repeat=3)),
        "hash set": min(timeit.repeat(lambda: [q in as_set for q in queries], number=1, repeat=3)),
    }


def choose_structure(*, need_order: bool, on_disk: bool = False, prefix_queries: bool = False,
                     read_heavy: bool = False, changes_often: bool = True) -> str:
    """The chapter's decision tree."""
    if prefix_queries:
        return "trie"
    if on_disk:
        return "B+ tree"
    if not need_order:
        return "hash table"
    if not changes_often:
        return "sorted array + binary search"
    return "AVL tree" if read_heavy else "red-black tree (library sorted map)"


if __name__ == "__main__":
    for name, row in height_table(5000).items():
        print(f"{name:>20}: {row}")
    print({k: round(v, 5) for k, v in lookup_race(20000).items()})
    print(choose_structure(need_order=False), "|", choose_structure(need_order=True), "|",
          choose_structure(need_order=True, on_disk=True), "|", choose_structure(need_order=True, prefix_queries=True))
