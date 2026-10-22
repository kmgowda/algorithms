"""Volume 3, Chapter 23 - Treaps.

A treap is a binary search tree by key and a max-heap by a random priority (Figure 23.2). Insert attaches a leaf
and rotates it up while its priority beats its parent's (Figure 23.3); delete rotates a key down below the child
with the higher priority until it can be cut out (Figure 23.4). Split and merge (Figure 23.5) give a second way to
insert and delete. With random priorities every key has expected depth H_k + H_(n-k+1) - 2 < 2 ln n + 1
(Section 23.7, Figure 23.6), whatever order the keys arrive in.

Priorities are either given explicitly (a dict key -> priority, as for the printed figures) or drawn from a seeded
random generator, so every number in the chapter can be reproduced.

Run:  python3 ch23_examples.py
"""

from __future__ import annotations

import importlib.util
import math
import os
import random


class Node:
    __slots__ = ("key", "prio", "left", "right")

    def __init__(self, key, prio):
        self.key, self.prio, self.left, self.right = key, prio, None, None


def rotate_right(t):
    """Lift t's left child above t; the inorder sequence is unchanged."""
    x = t.left
    t.left, x.right = x.right, t
    return x


def rotate_left(t):
    """Lift t's right child above t."""
    x = t.right
    t.right, x.left = x.left, t
    return x


def split(t, key):
    """Cut treap t into (keys < key, keys >= key), both treaps."""
    if t is None:
        return None, None
    if t.key < key:
        t.right, right = split(t.right, key)
        return t, right
    left, t.left = split(t.left, key)
    return left, t


def merge(a, b):
    """Every key of a is below every key of b: join them into one treap."""
    if a is None or b is None:
        return a or b
    if a.prio > b.prio:
        a.right = merge(a.right, b)
        return a
    b.left = merge(a, b.left)
    return b


class Treap:
    """`rotations` counts every rotation made by insert and delete; `last_rotations` those of the last update."""

    def __init__(self, keys=(), priorities=None, seed=None):
        self.root = None
        self.rotations = self.last_rotations = 0
        self.priorities = dict(priorities or {})
        self.rng = random.Random(seed)
        for k in keys:
            self.insert(k)

    def priority_for(self, key):
        """The printed priority if one was given, otherwise a fresh random roll."""
        return self.priorities[key] if key in self.priorities else self.rng.random()

    def _rotate_right(self, t):
        self.rotations += 1
        self.last_rotations += 1
        return rotate_right(t)

    def _rotate_left(self, t):
        self.rotations += 1
        self.last_rotations += 1
        return rotate_left(t)

    def contains(self, key) -> bool:
        t = self.root
        while t is not None and t.key != key:
            t = t.left if key < t.key else t.right
        return t is not None

    def insert(self, key, prio=None) -> bool:
        """Insert key (a duplicate is refused: returns False). Rotations are counted in last_rotations."""
        self.last_rotations = 0
        if self.contains(key):
            return False
        self.root = self._insert(self.root, key, self.priority_for(key) if prio is None else prio)
        return True

    def _insert(self, t, key, prio):
        if t is None:
            return Node(key, prio)
        if key < t.key:
            t.left = self._insert(t.left, key, prio)
            if t.left.prio > t.prio:              # heap order broken: lift the new child
                t = self._rotate_right(t)
        else:
            t.right = self._insert(t.right, key, prio)
            if t.right.prio > t.prio:
                t = self._rotate_left(t)
        return t

    def delete(self, key) -> bool:
        """Rotate key down below its higher-priority child until it has at most one child, then cut it out."""
        self.last_rotations = 0
        if not self.contains(key):
            return False
        self.root = self._delete(self.root, key)
        return True

    def _delete(self, t, key):
        if key < t.key:
            t.left = self._delete(t.left, key)
        elif key > t.key:
            t.right = self._delete(t.right, key)
        elif t.left is None:
            return t.right
        elif t.right is None:
            return t.left
        elif t.left.prio > t.right.prio:          # the higher-priority child moves up
            t = self._rotate_right(t)
            t.right = self._delete(t.right, key)
        else:
            t = self._rotate_left(t)
            t.left = self._delete(t.left, key)
        return t

    # ---------------------------------------------------------------- the split-and-merge versions

    def insert_by_split(self, key, prio=None) -> bool:
        """Insert with no rotations: split at key, then merge left, the new node, and right."""
        if self.contains(key):
            return False
        left, right = split(self.root, key)
        node = Node(key, self.priority_for(key) if prio is None else prio)
        self.root = merge(merge(left, node), right)
        return True

    def delete_by_merge(self, key) -> bool:
        """Find key and replace its node by the merge of its two subtrees."""
        parent, t = None, self.root
        while t is not None and t.key != key:
            parent, t = t, (t.left if key < t.key else t.right)
        if t is None:
            return False
        joined = merge(t.left, t.right)
        if parent is None:
            self.root = joined
        elif parent.left is t:
            parent.left = joined
        else:
            parent.right = joined
        return True

    # ---------------------------------------------------------------- inspection

    def shape(self, t="root", prio=False):
        """(key, left, right) tuples for drawing; with prio=True each key is a (key, priority) pair."""
        t = self.root if t == "root" else t
        if t is None:
            return None
        return ((t.key, t.prio) if prio else t.key, self.shape(t.left, prio), self.shape(t.right, prio))

    def keys(self):
        out = []

        def walk(t):
            if t:
                walk(t.left)
                out.append(t.key)
                walk(t.right)
        walk(self.root)
        return out

    def height(self, t="root") -> int:
        t = self.root if t == "root" else t
        return -1 if t is None else 1 + max(self.height(t.left), self.height(t.right))

    def depth(self, key) -> int:
        d, t = 0, self.root
        while t.key != key:
            t = t.left if key < t.key else t.right
            d += 1
        return d

    def depths(self) -> dict:
        out = {}

        def walk(t, d):
            if t:
                out[t.key] = d
                walk(t.left, d + 1)
                walk(t.right, d + 1)
        walk(self.root, 0)
        return out

    def valid(self) -> bool:
        return is_treap(self.root)


def is_treap(t) -> bool:
    """BST order on the keys (strict) and heap order on the priorities (no child above its parent)."""
    def ok(t, lo, hi):
        if t is None:
            return True
        if (lo is not None and t.key <= lo) or (hi is not None and t.key >= hi):
            return False
        for c in (t.left, t.right):
            if c is not None and c.prio > t.prio:
                return False
        return ok(t.left, lo, t.key) and ok(t.right, t.key, hi)
    return ok(t, None, None)


def from_root(root) -> Treap:
    """Wrap a node (for example one half of a split) as a Treap."""
    t = Treap()
    t.root = root
    return t


def plain_bst_shape(keys):
    """Shape of the plain BST (Chapter 5) built by inserting keys in the given order, no rotations."""
    root = None

    def ins(t, k):
        if t is None:
            return [k, None, None]
        if k < t[0]:
            t[1] = ins(t[1], k)
        else:
            t[2] = ins(t[2], k)
        return t
    for k in keys:
        root = ins(root, k)

    def freeze(t):
        return None if t is None else (t[0], freeze(t[1]), freeze(t[2]))
    return freeze(root)


def priority_order_bst(priorities: dict):
    """The uniqueness theorem's tree: insert the keys into a plain BST from the highest priority down."""
    return plain_bst_shape(sorted(priorities, key=priorities.get, reverse=True))


def harmonic(n: int) -> float:
    return sum(1 / i for i in range(1, n + 1))


def expected_depth(n: int, k: int) -> float:
    """E[depth of the k-th smallest of n keys] = H_k + H_(n-k+1) - 2 (Section 23.7)."""
    return harmonic(k) + harmonic(n - k + 1) - 2


def depth_experiment(keys, trials: int, seed: int = 1):
    """Average depth of each key over `trials` treaps built from keys (in the given order) with random priorities,
    beside the formula. Returns a list of (key, measured, formula)."""
    rng = random.Random(seed)
    total = {k: 0 for k in keys}
    for _ in range(trials):
        t = Treap(keys, seed=rng.random())
        for k, d in t.depths().items():
            total[k] += d
    ranks = {k: i + 1 for i, k in enumerate(sorted(keys))}
    return [(k, total[k] / trials, expected_depth(len(keys), ranks[k])) for k in sorted(keys)]


def rotations_per_insert(keys, seed: int = 1) -> float:
    t = Treap(keys, seed=seed)
    return t.rotations / max(1, len(keys))


def rotation_experiment(n: int, trials: int, seed: int = 1):
    """Build `trials` treaps of n shuffled keys; return (measured rotations per insertion, the exact expectation).
    Inserting the k-th smallest of m keys makes 2 - 1/k - 1/(m-k+1) rotations on average (Section 23.7); with k
    uniform that is 2 - 2 H_m / m, averaged over m = 1..n."""
    rng, total = random.Random(seed), 0
    for _ in range(trials):
        keys = list(range(n))
        rng.shuffle(keys)
        total += Treap(keys, seed=rng.random()).rotations
    exact = sum(2 - 2 * harmonic(m) / m for m in range(1, n + 1)) / n
    return total / (trials * n), exact


def spine_rotations(t: Treap, key) -> int:
    """Length of the right spine of key's left subtree plus the left spine of its right subtree: the number of
    rotations that inserting key made (Section 23.7)."""
    n = t.root
    while n.key != key:
        n = n.left if key < n.key else n.right
    count, a = 0, n.left
    while a:
        count, a = count + 1, a.right
    b = n.right
    while b:
        count, b = count + 1, b.left
    return count


def _load(folder, module):
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), folder, module + ".py")
    spec = importlib.util.spec_from_file_location(f"ch23_uses_{module}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def library_comparison(seed: int = 1) -> dict:
    """Section 23.8: treap, red-black tree (Chapter 8) and splay tree (Chapter 22) on the library's data.
    Sorted: 1,000 call numbers in increasing order. Random: 10,000 keys in a shuffled order.
    Returns {structure: (height when sorted, height when shuffled, average depth when shuffled)}."""
    rb, sp = _load("chapter_08_red_black", "ch08_examples"), _load("chapter_22_splay_trees", "ch22_examples")
    sorted_keys = list(range(1, 1001))
    keys = list(range(10_000))
    random.Random(seed).shuffle(keys)
    out = {}
    for name, build in (("treap", lambda ks, i: Treap(ks, seed=seed + i).root),
                        ("red-black", lambda ks, i: rb.RedBlackTree(ks).root),
                        ("splay", lambda ks, i: sp.SplayTree(ks).root)):
        d_sorted, d = node_depths(build(sorted_keys, 0)), node_depths(build(keys, 1))
        out[name] = (max(d_sorted), max(d), sum(d) / len(d))
    return out


def node_depths(root) -> list:
    """Depth of every node of any binary tree with .left and .right (no recursion: paths can be long)."""
    out, stack = [], [(root, 0)] if root else []
    while stack:
        n, d = stack.pop()
        out.append(d)
        stack.extend((c, d + 1) for c in (n.left, n.right) if c)
    return out
    return out


SHELF = [12, 25, 31, 47, 58, 63, 70, 84, 91]
RETURNS = [58, 25, 91, 12, 70, 47, 84, 31, 63]
# The printed dice rolls of the chapter's figures: each catalogue card's priority.
ROLLS = {12: 41, 25: 77, 31: 18, 47: 63, 58: 95, 63: 29, 70: 84, 84: 52, 91: 36}


def shelf_treap(order=SHELF) -> Treap:
    return Treap(order, priorities=ROLLS)


if __name__ == "__main__":
    t = shelf_treap()
    print("shelf in sorted order:", t.shape(), "height", t.height(), "rotations", t.rotations)
    print("returns pile gives the same tree:", shelf_treap(RETURNS).shape() == t.shape())
    print("equals the BST built in priority order:", priority_order_bst(ROLLS) == t.shape())
    for k, m, f in depth_experiment(SHELF, 20_000):
        print(f"  depth of {k}: measured {m:.3f}, formula {f:.3f}")
    print("rotations per insert, 200 builds of 1,000 shuffled keys (measured, exact):", rotation_experiment(1000, 200))
    print("rotations per insert, 10,000 sorted keys:", rotations_per_insert(range(10_000)))
    for name, row in library_comparison().items():
        print(name, [round(v, 2) for v in row])
