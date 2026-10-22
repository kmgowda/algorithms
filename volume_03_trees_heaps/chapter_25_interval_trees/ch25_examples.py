"""Volume 3, Chapter 25 - Interval Trees.

A binary search tree of closed intervals [start, end], keyed by start (ties broken by end), in which every node
also stores `max`, the largest end anywhere in its subtree (Figure 25.2). The field is recomputed from a node
and its two children, so insertions, deletions and rotations keep it correct (Section 25.7). With it, one
overlapping interval is found on a single root-to-leaf path (Section 25.5), and all k of them in O((k + 1) h).

`visited` counts the nodes whose interval a query compares, to show the pruning (Figures 25.3 and 25.5).

Run:  python3 ch25_examples.py
"""

from __future__ import annotations

import random

# Study-room bookings in Maya's library: (first day, last day, group), closed intervals of day numbers.
BOOKINGS = [(12, 15, "chess club"), (5, 11, "exam group"), (20, 24, "film society"), (3, 7, "tutors"),
            (9, 14, "book club"), (16, 18, "code club"), (25, 28, "choir"), (1, 2, "knitters")]
CLOSURE = (14, 17)          # the repairs: which bookings overlap days 14 to 17?


class Node:
    __slots__ = ("start", "end", "name", "max", "left", "right")

    def __init__(self, start, end, name=None):
        self.start, self.end, self.name = start, end, name
        self.max = end
        self.left = self.right = None

    def fix(self):
        """The augmentation rule: max is computed from this node and its two children only."""
        self.max = self.end
        for c in (self.left, self.right):
            if c is not None and c.max > self.max:
                self.max = c.max

    def interval(self):
        return (self.start, self.end)


def rotate_right(y):
    """Lift y's left child x above y; only y and x change their subtrees, so fix y first, then x."""
    x = y.left
    y.left, x.right = x.right, y
    y.fix()
    x.fix()
    return x


def rotate_left(x):
    y = x.right
    x.right, y.left = y.left, x
    x.fix()
    y.fix()
    return y


class IntervalTree:
    def __init__(self, intervals=()):
        self.root = None
        self.visited = 0
        for iv in intervals:
            self.insert(*iv)

    @classmethod
    def balanced(cls, intervals):
        """Build a perfectly balanced tree from the sorted intervals (upper medians as roots), fixing bottom-up."""
        items = sorted(intervals, key=lambda iv: (iv[0], iv[1]))

        def build(lo, hi):
            if lo > hi:
                return None
            m = (lo + hi + 1) // 2               # the upper median
            x = Node(*items[m][:2], items[m][2] if len(items[m]) > 2 else None)
            x.left, x.right = build(lo, m - 1), build(m + 1, hi)
            x.fix()
            return x
        t = cls()
        t.root = build(0, len(items) - 1)
        return t

    def insert(self, start, end, name=None):
        """Insert [start, end] (duplicates allowed, placed on the right) and fix max on the way back up."""
        if start > end:
            raise ValueError("an interval needs start <= end")

        def ins(x):
            if x is None:
                return Node(start, end, name)
            if (start, end) < (x.start, x.end):
                x.left = ins(x.left)
            else:
                x.right = ins(x.right)
            x.fix()
            return x
        self.root = ins(self.root)

    def delete(self, start, end):
        """Remove one copy of [start, end]; returns True if it was there. Every node on the path is fixed."""
        found = False

        def remove_min(x):                       # returns (subtree without its minimum, the minimum node)
            if x.left is None:
                return x.right, x
            x.left, m = remove_min(x.left)
            x.fix()
            return x, m

        def dele(x):
            nonlocal found
            if x is None:
                return None
            if (start, end) < (x.start, x.end):
                x.left = dele(x.left)
            elif (start, end) > (x.start, x.end):
                x.right = dele(x.right)
            else:
                found = True
                if x.left is None or x.right is None:
                    return x.left or x.right
                x.right, m = remove_min(x.right)  # the successor takes x's place
                m.left, m.right = x.left, x.right
                x = m
            x.fix()
            return x
        self.root = dele(self.root)
        return found

    def find_overlap(self, lo, hi):
        if lo > hi:                            # an empty query overlaps nothing
            return None
        x = self.root
        while x is not None:
            self.visited += 1
            if x.start <= hi and lo <= x.end:
                return x
            if x.left is not None and x.left.max >= lo:
                x = x.left                     # no overlap on the left means none on the right
            else:
                x = x.right                    # every interval on the left ends before lo
        return None

    def all_overlaps(self, lo, hi):
        out = []

        def walk(x):
            if x is None or x.max < lo:        # nothing below x ends late enough
                return
            self.visited += 1
            walk(x.left)
            if x.start <= hi and lo <= x.end:
                out.append(x.interval())
            if x.start <= hi:                  # the right subtree starts even later
                walk(x.right)
        if lo <= hi:
            walk(self.root)
        return out

    # ------------------------------------------------------------ checks and pictures
    def valid(self):
        """BST order on (start, end) and max correct at every node."""
        def check(x, lo, hi):
            if x is None:
                return True, float("-inf")
            k = (x.start, x.end)
            if x.start > x.end or (lo is not None and k < lo) or (hi is not None and k > hi):
                return False, 0
            ok_l, m_l = check(x.left, lo, k)
            ok_r, m_r = check(x.right, k, hi)
            return ok_l and ok_r and x.max == max(x.end, m_l, m_r), x.max
        return check(self.root, None, None)[0]

    def intervals(self):
        out = []

        def walk(x):
            if x:
                walk(x.left)
                out.append(x.interval())
                walk(x.right)
        walk(self.root)
        return out

    def height(self):
        def h(x):
            return -1 if x is None else 1 + max(h(x.left), h(x.right))
        return h(self.root)

    def shape(self, x="root"):
        """Nested ((start, end, max), left, right) for drawing and tests."""
        x = self.root if x == "root" else x
        if x is None:
            return None
        return ((x.start, x.end, x.max), self.shape(x.left), self.shape(x.right))


def shape_of(x):
    if x is None:
        return None
    return ((x.start, x.end, x.max), shape_of(x.left), shape_of(x.right))


def brute_overlaps(intervals, lo, hi):
    """The O(n) check every query is tested against."""
    return sorted((a, b) for a, b, *_ in intervals if a <= hi and lo <= b and lo <= hi)


def random_bookings(n, days=365, longest=7, seed=1):
    rng = random.Random(seed)
    out = []
    for _ in range(n):
        a = rng.randrange(1, days + 1)
        out.append((a, min(days, a + rng.randrange(longest))))
    return out


def measure(n=1000, query=(100, 103), seed=1):
    """Worked problem (Section 25.8): nodes compared by find_overlap and all_overlaps in a balanced tree."""
    data = random_bookings(n, seed=seed)
    t = IntervalTree.balanced(data)
    t.find_overlap(*query)
    one = t.visited
    t.visited = 0
    found = t.all_overlaps(*query)
    return {"n": n, "height": t.height(), "find_one": one, "k": len(found), "all": t.visited}


if __name__ == "__main__":
    t = IntervalTree(BOOKINGS)
    print("tree:", t.shape(), "valid", t.valid())
    print("all overlaps of", CLOSURE, t.all_overlaps(*CLOSURE), "nodes compared", t.visited)
    for q in [(17, 19), (29, 30), (8, 8)]:
        t.visited = 0
        x = t.find_overlap(*q)
        print("find one", q, x and x.interval(), "nodes", t.visited)
    print("1,000 random bookings:", measure())
