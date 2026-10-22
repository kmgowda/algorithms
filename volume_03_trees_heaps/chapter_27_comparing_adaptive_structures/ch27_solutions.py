"""Volume 3, Chapter 27 - Thinking Problems (Section 27.17).

k_nearest: the k nearest points of a k-d tree (Chapter 26) with a bounded max-heap (Chapter 15), Thinking
Problem 2.  treap_versus_root: the cost of searching a red-black tree's root key again and again, against the
expected cost of the same key in a treap (Thinking Problem 1).
"""

from __future__ import annotations

import heapq
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ch27_examples as ex  # noqa: E402


def k_nearest(tree, q, k):
    """The k points of tree nearest to q, nearest first, as (squared distance, point); also sets tree.visited."""
    if k <= 0:
        return []
    best = []                                     # max-heap of the k best so far, as (-d2, point)

    def visit(x):
        if x is None:
            return
        tree.visited += 1
        d2 = ex.kd.dist2(x.point, q)
        if len(best) < k:
            heapq.heappush(best, (-d2, x.point))
        elif d2 < -best[0][0]:
            heapq.heapreplace(best, (-d2, x.point))   # drop the worst of the k
        diff = q[x.axis] - x.point[x.axis]
        near, far = (x.left, x.right) if diff < 0 else (x.right, x.left)
        visit(near)
        if len(best) < k or diff * diff < -best[0][0]:  # the k-th best circle crosses the line
            visit(far)
    visit(tree.root)
    return sorted((-nd, p) for nd, p in best)


def brute_k_nearest(points, q, k):
    return sorted((ex.kd.dist2(p, q), tuple(p)) for p in points)[:max(k, 0)]


def treap_versus_root(n: int = 10_000, seed: int = 1):
    """Build a red-black tree from n shuffled keys; its root key costs 1 comparison per search. Return
    (root key, its rank k from 1, the treap's expected comparisons H_k + H_(n-k+1) - 1, the bound 2 ln n + 1)."""
    keys = list(range(n))
    random.Random(seed).shuffle(keys)
    root = ex.rb.RedBlackTree(keys).root.key
    k = root + 1
    import math
    return root, k, ex.tr.expected_depth(n, k) + 1, 2 * math.log(n) + 1
