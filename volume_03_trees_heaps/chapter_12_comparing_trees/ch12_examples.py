"""Volume 3, Chapter 12 - Comparing Trees.

Loads the same keys into the trees of Part I (and a hash set) and measures them.
Run:  python3 ch12_examples.py
"""

from __future__ import annotations

import os
import random
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
for folder in ("chapter_05_bst", "chapter_07_avl", "chapter_08_red_black", "chapter_09_b_trees"):
    sys.path.insert(0, os.path.join(HERE, "..", folder))

import ch05_examples as bst  # noqa: E402
import ch07_examples as avl  # noqa: E402
import ch08_examples as rb  # noqa: E402
import ch09_examples as bt  # noqa: E402


def _avl_contains(root, key) -> bool:
    n = root
    while n is not None:
        if key == n.key:
            return True
        n = n.left if key < n.key else n.right
    return False


def _rb_contains(tree, key) -> bool:
    n = tree.root
    while n is not None:
        if key == n.key:
            return True
        n = n.left if key < n.key else n.right
    return False


def measure(keys: list[int], lookups: list[int]) -> dict[str, dict]:
    """Build each structure from keys, then look up every key in lookups. Times in milliseconds."""
    results = {}

    def run(name, build, contains, height):
        t0 = time.perf_counter()
        s = build()
        t1 = time.perf_counter()
        found = sum(contains(s, k) for k in lookups)
        t2 = time.perf_counter()
        results[name] = {"build ms": round((t1 - t0) * 1000, 1), "lookup ms": round((t2 - t1) * 1000, 1),
                         "height": height(s), "found": found}

    run("plain BST", lambda: bst.BST(keys), lambda s, k: s.contains(k), lambda s: s.height())
    run("AVL", lambda: avl.build(keys), _avl_contains, avl.h)
    run("red-black", lambda: rb.RedBlackTree(keys), _rb_contains, lambda s: s.height())
    run("B-tree (63 keys/node)", lambda: bt.BTree(63, keys), lambda s, k: s.search(k)[0], lambda s: s.height())
    run("hash set", lambda: set(keys), lambda s, k: k in s, lambda s: None)
    return results


def repair_work(keys: list[int]) -> dict[str, int]:
    """Count the repair work behind the build times of Section 12.5: AVL rotations and the stored heights
    it recomputes on the way back up every insert, against red-black rotations."""
    counts = {"AVL rotations": 0, "AVL height updates": 0}
    update, left, right = avl.update, avl.rotate_left, avl.rotate_right

    def counted_update(n):
        counts["AVL height updates"] += 1
        update(n)

    def counted_left(x):
        counts["AVL rotations"] += 1
        return left(x)

    def counted_right(y):
        counts["AVL rotations"] += 1
        return right(y)
    avl.update, avl.rotate_left, avl.rotate_right = counted_update, counted_left, counted_right
    try:
        avl.build(keys)
    finally:
        avl.update, avl.rotate_left, avl.rotate_right = update, left, right
    counts["red-black rotations"] = rb.RedBlackTree(keys).rotations
    return counts


if __name__ == "__main__":
    sys.setrecursionlimit(30_000)
    rng = random.Random(1)
    n = 10_000
    rand_keys = rng.sample(range(10 ** 6), n)
    for label, keys in (("random arrivals", rand_keys), ("sorted arrivals", sorted(rand_keys))):
        print(label)
        for name, r in measure(keys, rand_keys).items():
            print(f"  {name:24s} {r}")
        print("  repair work", repair_work(keys))
