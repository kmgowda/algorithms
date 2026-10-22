"""Volume 3, Chapter 26 - k-d Trees: companion code for the Thinking Problems (Section 26.16).

Run:  python3 ch26_solutions.py
"""

from __future__ import annotations

import math

from ch26_examples import KDTree, dist2

INF = math.inf


def median_height(n: int) -> int:
    """Thinking Problem 1: the height of a k-d tree built by medians from n points (claimed: floor(log2 n))."""
    return KDTree([(i * 7 % (n + 3), i) for i in range(n)]).height()


def subtree_sizes(tree: KDTree) -> dict:
    """{id(node): number of points in its subtree}, the extra field of Thinking Problem 2."""
    sizes = {}

    def walk(x):
        if x is None:
            return 0
        sizes[id(x)] = 1 + walk(x.left) + walk(x.right)
        return sizes[id(x)]
    walk(tree.root)
    return sizes


def range_count(tree: KDTree, lo, hi, sizes=None) -> int:
    """Thinking Problem 2: how many points lie in the closed box [lo, hi], without listing them.
    A subtree whose region misses the box adds 0, one whose region lies inside it adds its size."""
    sizes = subtree_sizes(tree) if sizes is None else sizes
    d = tree.dims

    def count(x, rlo, rhi):
        if x is None or any(rhi[i] < lo[i] or rlo[i] > hi[i] for i in range(d)):
            return 0                                           # the region misses the box
        tree.visited += 1
        if all(lo[i] <= rlo[i] and rhi[i] <= hi[i] for i in range(d)):
            return sizes[id(x)]                                # the region lies inside the box
        a, p = x.axis, x.point
        here = 1 if all(lo[i] <= p[i] <= hi[i] for i in range(d)) else 0
        left_hi = rhi[:a] + (p[a],) + rhi[a + 1:]
        right_lo = rlo[:a] + (p[a],) + rlo[a + 1:]
        return here + count(x.left, rlo, left_hi) + count(x.right, right_lo, rhi)
    if any(lo[i] > hi[i] for i in range(d)):
        return 0
    return count(tree.root, (-INF,) * d, (INF,) * d)


def nearest_far_child_rule(tree: KDTree, q):
    """Thinking Problem 3, the buggy rule: visit the far side only if the far CHILD's point beats the best."""
    best = [None, INF]

    def visit(x):
        if x is None:
            return
        d2 = dist2(x.point, q)
        if d2 < best[1]:
            best[0], best[1] = x.point, d2
        diff = q[x.axis] - x.point[x.axis]
        near, far = (x.left, x.right) if diff < 0 else (x.right, x.left)
        visit(near)
        if far is not None and dist2(far.point, q) < best[1]:
            visit(far)
    visit(tree.root)
    return best[0], best[1]


if __name__ == "__main__":
    from ch26_examples import BRANCHES, NAME
    print([median_height(n) for n in range(1, 17)])
    t = KDTree(BRANCHES.values())
    print("count in (6,3)-(9,9):", range_count(t, (6, 3), (9, 9)), "opened", t.visited)
    p, d2 = nearest_far_child_rule(t, (1, 7))
    print("buggy rule at (1, 7):", NAME[p], d2, " correct:", NAME[t.nearest((1, 7))[0]])
