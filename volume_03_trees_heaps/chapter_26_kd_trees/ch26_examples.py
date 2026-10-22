"""Volume 3, Chapter 26 - k-d Trees.

A binary tree of points in which the levels split the plane alternately by x and by y (in d dimensions, by
coordinates 0, 1, ..., d - 1 in turn). Invariant: every point in a node's left subtree has a coordinate on the
node's axis <= the node's, every point in its right subtree >= the node's. Built by medians (Section 26.4); range
search (Section 26.5) and nearest-neighbour search (Section 26.6) prune whole subtrees.

`visited` counts the nodes a query opens, to show the pruning (Figures 26.3 and 26.5).

Run:  python3 ch26_examples.py
"""

from __future__ import annotations

import random

# Maya's library branches on the town map, (x, y) in hundreds of metres east and north of the south-west corner.
BRANCHES = {"Abbey": (1, 6), "Park": (2, 2), "Castle": (3, 7), "Orchard": (4, 9), "Market": (5, 4),
            "Station": (6, 1), "Hilltop": (7, 8), "Wharf": (8, 5), "Riverside": (9, 2)}
NAME = {p: n for n, p in BRANCHES.items()}
READER = (7, 4)                 # a reader on Bridge Street: which branch is nearest?
BOX = ((6, 3), (9, 9))          # the east-side rectangle: x from 6 to 9, y from 3 to 9


class KDNode:
    __slots__ = ("point", "axis", "left", "right")

    def __init__(self, point, axis):
        self.point, self.axis = point, axis
        self.left = self.right = None


def build(points, depth=0):
    if not points:
        return None
    axis = depth % len(points[0])
    points = sorted(points, key=lambda p: p[axis])
    m = len(points) // 2                  # the median splits the points in half
    node = KDNode(points[m], axis)
    node.left = build(points[:m], depth + 1)
    node.right = build(points[m + 1:], depth + 1)
    return node


def dist2(p, q):
    return sum((a - b) ** 2 for a, b in zip(p, q))


class KDTree:
    def __init__(self, points=(), dims=None):
        points = [tuple(p) for p in points]
        self.dims = dims or (len(points[0]) if points else 2)
        self.root = build(points)
        self.visited = 0

    def insert(self, p):
        """Walk down as in a BST, comparing on each node's axis (equal goes right); the new leaf splits on the
        next axis."""
        p = tuple(p)
        if self.root is None:
            self.root = KDNode(p, 0)
            return
        x = self.root
        while True:
            side = "left" if p[x.axis] < x.point[x.axis] else "right"
            child = getattr(x, side)
            if child is None:
                setattr(x, side, KDNode(p, (x.axis + 1) % self.dims))
                return
            x = child

    def find_min(self, x, axis):
        """The point with the smallest coordinate on `axis` in x's subtree; one side only where x splits on axis."""
        if x is None:
            return None
        best = x.point
        kids = [x.left] if x.axis == axis else [x.left, x.right]
        for c in kids:
            m = self.find_min(c, axis)
            if m is not None and m[axis] < best[axis]:
                best = m
        return best

    def delete(self, p):
        """Remove one copy of p; returns True if it was there. A deleted node takes the smallest point on its axis
        from its right subtree (or, with no right subtree, from its left, which then becomes the right)."""
        p = tuple(p)

        def dele(x, p):
            if x is None:
                return None, False
            a = x.axis
            if x.point == p:
                if x.right is not None:
                    m = self.find_min(x.right, a)
                    x.point = m
                    x.right, _ = dele(x.right, m)
                elif x.left is not None:
                    m = self.find_min(x.left, a)
                    x.point = m
                    x.right, _ = dele(x.left, m)
                    x.left = None
                else:
                    return None, True
                return x, True
            done = False
            if p[a] <= x.point[a]:                     # an equal coordinate may sit on either side
                x.left, done = dele(x.left, p)
            if not done and p[a] >= x.point[a]:
                x.right, done = dele(x.right, p)
            return x, done
        self.root, ok = dele(self.root, p)
        return ok

    def range_search(self, lo, hi):
        """Every point p with lo[i] <= p[i] <= hi[i] on every axis (a closed box)."""
        out = []

        def visit(x):
            if x is None:
                return
            self.visited += 1
            p, a = x.point, x.axis
            if all(l <= c <= h for l, c, h in zip(lo, p, hi)):
                out.append(p)
            if lo[a] <= p[a]:                  # the box reaches the left side of the line
                visit(x.left)
            if p[a] <= hi[a]:                  # the box reaches the right side
                visit(x.right)
        visit(self.root)
        return out

    def nearest(self, q):
        best = [None, float("inf")]            # the best point so far and its squared distance

        def visit(x):
            if x is None:
                return
            self.visited += 1
            d2 = dist2(x.point, q)
            if d2 < best[1]:
                best[0], best[1] = x.point, d2
            diff = q[x.axis] - x.point[x.axis]
            near, far = (x.left, x.right) if diff < 0 else (x.right, x.left)
            visit(near)                        # the side of the line q is on
            if diff * diff < best[1]:          # the best circle crosses the line
                visit(far)
        visit(self.root)
        return best[0], best[1]

    # ------------------------------------------------------------ checks and pictures
    def points(self):
        out = []

        def walk(x):
            if x:
                walk(x.left)
                out.append(x.point)
                walk(x.right)
        walk(self.root)
        return out

    def valid(self):
        """The k-d invariant at every node, and axes cycling 0, 1, ..., d - 1 with depth."""
        def sub(x):
            return [] if x is None else sub(x.left) + [x.point] + sub(x.right)

        def check(x, depth):
            if x is None:
                return True
            a = x.axis
            if a != depth % self.dims:
                return False
            if any(p[a] > x.point[a] for p in sub(x.left)) or any(p[a] < x.point[a] for p in sub(x.right)):
                return False
            return check(x.left, depth + 1) and check(x.right, depth + 1)
        return check(self.root, 0)

    def height(self):
        def h(x):
            return -1 if x is None else 1 + max(h(x.left), h(x.right))
        return h(self.root)

    def shape(self, x="root"):
        x = self.root if x == "root" else x
        if x is None:
            return None
        return ((x.point, "xyz"[x.axis] if x.axis < 3 else x.axis), self.shape(x.left), self.shape(x.right))

    def regions(self, box=((0, 0), (10, 10))):
        """[(point, axis, region box)] for every node in preorder; regions are closed boxes (2-D drawing)."""
        out = []

        def walk(x, lo, hi):
            if x is None:
                return
            out.append((x.point, x.axis, (lo, hi)))
            a = x.axis
            l_hi, r_lo = list(hi), list(lo)
            l_hi[a] = r_lo[a] = x.point[a]
            walk(x.left, lo, tuple(l_hi))
            walk(x.right, tuple(r_lo), hi)
        walk(self.root, tuple(box[0]), tuple(box[1]))
        return out


def brute_range(points, lo, hi):
    return sorted(tuple(p) for p in points if all(l <= c <= h for l, c, h in zip(lo, p, hi)))


def brute_nearest(points, q):
    return min(dist2(p, q) for p in points) if points else float("inf")


def nearest_trace(tree, q):
    """[(point visited, squared distance, best squared distance after it)] in visiting order (Figure 26.5)."""
    trace, best = [], [float("inf")]

    def visit(x):
        if x is None:
            return
        d2 = dist2(x.point, q)
        best[0] = min(best[0], d2)
        trace.append((x.point, d2, best[0]))
        diff = q[x.axis] - x.point[x.axis]
        near, far = (x.left, x.right) if diff < 0 else (x.right, x.left)
        visit(near)
        if diff * diff < best[0]:
            visit(far)
    visit(tree.root)
    return trace


def line_regions(tree, x0, box=((0, 0), (1, 1))):
    """How many node regions the vertical line x = x0 meets (Figure 26.4, Section 26.5)."""
    return sum(1 for _, _, (lo, hi) in tree.regions(box) if lo[0] <= x0 <= hi[0])


def random_points(n, dims=2, seed=1):
    rng = random.Random(seed)
    return [tuple(rng.random() for _ in range(dims)) for _ in range(n)]


def nearest_cost(n, dims, queries=200, seed=1):
    """Average nodes opened by a nearest-neighbour search on n uniform random points (Section 26.7)."""
    t = KDTree(random_points(n, dims, seed), dims)
    rng = random.Random(seed + 1)
    for _ in range(queries):
        t.nearest(tuple(rng.random() for _ in range(dims)))
    return t.visited / queries


def line_cost(n, seed=1):
    t = KDTree(random_points(n, 2, seed))
    rng = random.Random(seed + 7)
    return sum(line_regions(t, rng.random()) for _ in range(20)) / 20


if __name__ == "__main__":
    t = KDTree(BRANCHES.values())
    print("tree:", t.shape(), "height", t.height(), "valid", t.valid())
    print("box", BOX, [NAME[p] for p in t.range_search(*BOX)], "opened", t.visited)
    t.visited = 0
    p, d2 = t.nearest(READER)
    print("nearest to", READER, NAME[p], d2, "opened", t.visited, nearest_trace(t, READER))
    for n in (64, 256, 1024, 4096, 16384):
        print("line regions", n, line_cost(n))
    for d in (2, 4, 8, 16):
        print("nearest, 10,000 points, d =", d, nearest_cost(10_000, d))
