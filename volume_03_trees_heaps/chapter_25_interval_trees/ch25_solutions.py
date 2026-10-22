"""Volume 3, Chapter 25 - Interval Trees: companion code for the Thinking Problems (Section 25.16).

Run:  python3 ch25_solutions.py
"""

from __future__ import annotations

from ch25_examples import IntervalTree


def overlaps(x, lo, hi):
    return x.start <= hi and lo <= x.end


def first_overlap(tree: IntervalTree, lo, hi):
    """Thinking Problem 1: the overlapping interval with the smallest (start, end), on one path, O(h)."""
    if lo > hi:
        return None
    best, x = None, tree.root
    while x is not None:
        tree.visited += 1
        if x.left is not None and x.left.max >= lo:
            if overlaps(x, lo, hi):
                best = x                       # a candidate; anything better is on the left
            x = x.left
        else:
            if overlaps(x, lo, hi):
                return x                       # nothing on the left overlaps, the right is later
            x = x.right
    return best


def covering(tree: IntervalTree, lo, hi):
    """Thinking Problem 2: one interval that contains all of [lo, hi], or None, in O(h).
    Among the intervals with start <= lo (the path to lo plus left subtrees hanging off it), take the largest end."""
    if lo > hi:
        return None
    best, node, sub = float("-inf"), None, None
    x = tree.root
    while x is not None:
        tree.visited += 1
        if x.start <= lo:                      # x and its whole left subtree start no later than lo
            if x.end > best:
                best, node, sub = x.end, x, None
            if x.left is not None and x.left.max > best:
                best, node, sub = x.left.max, None, x.left
            x = x.right
        else:                                  # x and its right subtree start after lo
            x = x.left
    if best < hi:
        return None
    while node is None:                        # walk down to the interval whose end is best
        tree.visited += 1
        if sub.end == best:
            node = sub
        elif sub.left is not None and sub.left.max == best:
            sub = sub.left
        else:
            sub = sub.right
    return node


def brute_covering(intervals, lo, hi):
    return [(a, b) for a, b, *_ in intervals if a <= lo and hi <= b and lo <= hi]


def spread_example(n: int, k: int):
    """Thinking Problem 3: n one-day bookings [i, i] except k evenly spaced long ones [i, n]; query [n, n].
    Returns (nodes opened by all_overlaps, height, number reported)."""
    step = n // k
    data = [(i, n if i % step == step // 2 and i // step < k else i) for i in range(n)]
    t = IntervalTree.balanced(data)
    found = t.all_overlaps(n, n)
    return t.visited, t.height(), len(found)


if __name__ == "__main__":
    from ch25_examples import BOOKINGS
    t = IntervalTree(BOOKINGS)
    print("find_overlap(14, 17):", t.find_overlap(14, 17).interval(), " first_overlap:",
          first_overlap(t, 14, 17).interval())
    print("covering(16, 17):", covering(t, 16, 17).interval(), " covering(13, 16):", covering(t, 13, 16))
    for n, k in [(1023, 1), (1023, 32), (1023, 128), (65535, 1024)]:
        print(n, k, spread_example(n, k))
