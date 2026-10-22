"""Volume 3, Chapter 12 - Comparing Trees: companion code for the Thinking Problems (Section 12.16).

Run:  python3 ch12_solutions.py
"""

from __future__ import annotations

import ch12_examples  # noqa: F401  (puts the Part I chapters on the import path)
import ch07_examples as avl
import ch08_examples as rb

AVL_TALLER = [10, 20, 30, 50, 100, 40, 80, 90, 60, 120, 110, 70]     # Thinking Problem 3


def merge_avl(a, b):
    """Thinking Problem 2: merge two AVL trees (Chapter 7 nodes) into one perfectly balanced AVL tree
    in O(m + n): list both inorder, merge the sorted lists, build from the middle (Chapter 11)."""
    xs, ys = avl.inorder(a), avl.inorder(b)
    keys, i, j = [], 0, 0
    while i < len(xs) or j < len(ys):
        if j == len(ys) or (i < len(xs) and xs[i] < ys[j]):
            k, i = xs[i], i + 1
        elif i == len(xs) or ys[j] < xs[i]:
            k, j = ys[j], j + 1
        else:                                             # the same key in both trees: keep one copy
            k, i, j = xs[i], i + 1, j + 1
        keys.append(k)

    def build(lo, hi):
        if lo > hi:
            return None
        mid = (lo + hi) // 2
        n = avl.Node(keys[mid])
        n.left, n.right = build(lo, mid - 1), build(mid + 1, hi)
        avl.update(n)                                     # children first, so every stored height is right
        return n
    return build(0, len(keys) - 1)


def heights(keys) -> tuple[int, int]:
    """(AVL height, red-black height) after inserting keys in this order."""
    return avl.h(avl.build(keys)), rb.RedBlackTree(keys).height()


if __name__ == "__main__":
    print(heights(AVL_TALLER), avl.shape(avl.build(AVL_TALLER)))
    print(rb.RedBlackTree(AVL_TALLER).shape())
    m = merge_avl(avl.build([12, 31, 58, 70, 91]), avl.build([25, 47, 63, 84]))
    print(avl.shape(m), avl.is_avl(m))
