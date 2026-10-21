"""Volume 2, Chapter 23 - Comparing Trees.

Loads the same keys into the trees of Part II (and a hash set) and measures them.
Run:  python3 ch23_examples.py
"""

from __future__ import annotations

import os
import random
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
for folder in ("chapter_16_bst", "chapter_18_avl", "chapter_19_red_black", "chapter_20_b_trees"):
    sys.path.insert(0, os.path.join(HERE, "..", folder))

import ch16_examples as bst  # noqa: E402
import ch18_examples as avl  # noqa: E402
import ch19_examples as rb  # noqa: E402
import ch20_examples as bt  # noqa: E402


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
    run("AVL", lambda: avl.build(keys), _avl_contains, lambda s: s.height)
    run("red-black", lambda: rb.RedBlackTree(keys), _rb_contains, lambda s: s.height())
    run("B-tree (63 keys/node)", lambda: bt.BTree(63, keys), lambda s, k: s.search(k)[0], lambda s: s.height())
    run("hash set", lambda: set(keys), lambda s, k: k in s, lambda s: None)
    return results


if __name__ == "__main__":
    sys.setrecursionlimit(30_000)
    rng = random.Random(1)
    n = 10_000
    rand_keys = rng.sample(range(10 ** 6), n)
    for label, keys in (("random arrivals", rand_keys), ("sorted arrivals", sorted(rand_keys))):
        print(label)
        for name, r in measure(keys, rand_keys).items():
            print(f"  {name:24s} {r}")
