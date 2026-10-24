"""Volume 3, Chapter 8 - Red-Black Trees.

Run:  python3 ch08_examples.py
"""

from __future__ import annotations

import random

RED, BLACK = "R", "B"


class Node:
    __slots__ = ("key", "colour", "left", "right", "parent")

    def __init__(self, key, colour=RED, parent=None):
        self.key, self.colour, self.left, self.right, self.parent = key, colour, None, None, parent


def colour(n) -> str:
    """An empty spot counts as black."""
    return BLACK if n is None else n.colour


def fewest_keys(height: int) -> int:
    """The fewest keys a red-black tree of this height (in edges) can hold. The sparsest tree has one long path
    alternating black and red, and every subtree hanging off it is a perfect all-black tree (Exercise 19.4)."""
    if height < 0:
        return 0
    return 3 * 2 ** (height // 2) - 2 if height % 2 == 0 else 2 ** ((height + 3) // 2) - 2


def tallest_height(n: int) -> int:
    """The greatest height a red-black tree with n keys can really reach (always below 2 log2(n + 1))."""
    h = -1
    while fewest_keys(h + 1) <= n:
        h += 1
    return h


class RedBlackTree:
    """Insertion with recolouring and rotations (Figures 8.3 and 8.4), deletion with the four sibling cases
    (Figures 8.5 and 8.6). `cases` logs the repairs of the most recent delete."""

    def __init__(self, keys=()):
        self.root = None
        self.rotations = 0
        self.recolours = 0
        self.cases = []
        for k in keys:
            self.insert(k)

    def _rotate_left(self, x):
        y = x.right
        x.right = y.left
        if y.left:
            y.left.parent = x
        self._replace(x, y)
        y.left, x.parent = x, y
        self.rotations += 1

    def _rotate_right(self, x):
        y = x.left
        x.left = y.right
        if y.right:
            y.right.parent = x
        self._replace(x, y)
        y.right, x.parent = x, y
        self.rotations += 1

    def _replace(self, old, new):
        new.parent = old.parent
        if old.parent is None:
            self.root = new
        elif old is old.parent.left:
            old.parent.left = new
        else:
            old.parent.right = new

    def insert(self, key) -> None:
        parent, n = None, self.root
        while n:
            if key == n.key:
                return
            parent, n = n, (n.left if key < n.key else n.right)
        z = Node(key, RED, parent)
        if parent is None:
            self.root = z
        elif key < parent.key:
            parent.left = z
        else:
            parent.right = z
        self._fix(z)

    def _fix(self, z):
        while z.parent and z.parent.colour == RED:
            p, g = z.parent, z.parent.parent
            uncle = g.right if p is g.left else g.left
            if uncle and uncle.colour == RED:          # case 1: red uncle -> recolour, move up
                p.colour = uncle.colour = BLACK
                g.colour = RED
                self.recolours += 1
                z = g
                continue
            if p is g.left:
                if z is p.right:                       # case 2: inside -> rotate into a line
                    self._rotate_left(p)
                    z, p = p, z
                self._rotate_right(g)                  # case 3: outside -> rotate grandparent
            else:
                if z is p.left:
                    self._rotate_right(p)
                    z, p = p, z
                self._rotate_left(g)
            p.colour, g.colour = BLACK, RED
            break
        self.root.colour = BLACK

    def find(self, key):
        n = self.root
        while n is not None and n.key != key:
            n = n.left if key < n.key else n.right
        return n

    def delete(self, key) -> bool:
        """Delete key as in a plain BST, then repair the missing black, if any. Returns False if key is absent."""
        self.cases = []
        z = self.find(key)
        if z is None:
            return False
        if z.left is not None and z.right is not None:   # two children: the successor's node is removed instead
            s = z.right
            while s.left is not None:
                s = s.left
            z.key, z = s.key, s
        child = z.left if z.left is not None else z.right  # z now has at most one child
        parent = z.parent
        if child is not None:
            child.parent = parent
        if parent is None:
            self.root = child
        elif z is parent.left:
            parent.left = child
        else:
            parent.right = child
        if z.colour == BLACK:                              # a black node left: one path is a black short
            if colour(child) == RED:
                child.colour = BLACK                       # a red child simply absorbs the extra black
                self.cases.append("red child")
            else:
                self._fix_delete(child, parent)
        return True

    def _fix_delete(self, x, parent):
        """x (possibly empty) carries an extra black; parent is its parent (Figure 8.6)."""
        while x is not self.root and colour(x) == BLACK:
            left = x is parent.left
            w = parent.right if left else parent.left        # the sibling: never empty here
            if w.colour == RED:                                # case 1: red sibling -> rotate, sibling turns black
                w.colour, parent.colour = BLACK, RED
                self._rotate_left(parent) if left else self._rotate_right(parent)
                self.cases.append(1)
                w = parent.right if left else parent.left
            near, far = (w.left, w.right) if left else (w.right, w.left)
            if colour(near) == BLACK and colour(far) == BLACK:  # case 2: pass the extra black up
                w.colour = RED
                self.recolours += 1
                self.cases.append(2)
                x, parent = parent, parent.parent
                continue
            if colour(far) == BLACK:                           # case 3: near red, far black -> turn into case 4
                near.colour, w.colour = BLACK, RED
                self._rotate_right(w) if left else self._rotate_left(w)
                self.cases.append(3)
                w = parent.right if left else parent.left
                near, far = (w.left, w.right) if left else (w.right, w.left)
            w.colour, parent.colour, far.colour = parent.colour, BLACK, BLACK   # case 4: far red -> rotate, done
            self._rotate_left(parent) if left else self._rotate_right(parent)
            self.cases.append(4)
            x = self.root
        if x is not None:
            x.colour = BLACK

    def black_height(self, n="root") -> int:
        """Black nodes on any path from n down to an empty spot, counting n itself if it is black (Figure 8.2)."""
        n = self.root if n == "root" else n
        count = 0
        while n is not None:
            count += n.colour == BLACK
            n = n.left
        return count

    def lemma_holds(self) -> bool:
        """The black-height lemma: every subtree whose root has black height b holds at least 2**b - 1 keys."""
        def size(n):
            if n is None:
                return 0
            s = 1 + size(n.left) + size(n.right)
            if s < 2 ** self.black_height(n) - 1:
                raise ValueError("lemma fails")
            return s
        try:
            size(self.root)
        except ValueError:
            return False
        return True

    def shape(self, n="root"):
        n = self.root if n == "root" else n
        return None if n is None else ((n.key, n.colour), self.shape(n.left), self.shape(n.right))

    def height(self, n="root") -> int:
        n = self.root if n == "root" else n
        return -1 if n is None else 1 + max(self.height(n.left), self.height(n.right))

    def inorder(self, n="root") -> list:
        n = self.root if n == "root" else n
        return [] if n is None else self.inorder(n.left) + [n.key] + self.inorder(n.right)

    def valid(self) -> bool:
        """Root black, no red node with a red child, same black count on every path."""
        def check(n):
            if n is None:
                return 1
            for c in (n.left, n.right):
                if n.colour == RED and c is not None and c.colour == RED:
                    raise ValueError("red-red")
            a, b = check(n.left), check(n.right)
            if a != b:
                raise ValueError("black heights differ")
            if (n.left and n.left.parent is not n) or (n.right and n.right.parent is not n):
                raise ValueError("parent link")
            return a + (n.colour == BLACK)
        try:
            check(self.root)
        except ValueError:
            return False
        return self.root is None or self.root.colour == BLACK


def random_deletions(n: int = 10_000, seed: int = 1):
    """Build a tree from n random keys, delete them all in random order: (rotations, most in one deletion,
    how often each repair case ran) (Section 8.6)."""
    rng = random.Random(seed)
    keys = rng.sample(range(10 ** 6), n)
    t = RedBlackTree(keys)
    order = keys[:]
    rng.shuffle(order)
    start, most, seen = t.rotations, 0, {}
    for k in order:
        r = t.rotations
        t.delete(k)
        most = max(most, t.rotations - r)
        for c in t.cases:
            seen[c] = seen.get(c, 0) + 1
    return t.rotations - start, most, seen


# AA trees (Arne Andersson, 1993): a node is [key, level, left, right]; a red node is a right child on the same level

def aa_skew(t):
    """A left child on the same level is not allowed: rotate right."""
    if t and t[2] and t[2][1] == t[1]:
        left = t[2]
        t[2], left[3] = left[3], t
        return left
    return t


def aa_split(t):
    """Two right children in a row on the same level are not allowed: rotate left and raise the middle node."""
    if t and t[3] and t[3][3] and t[3][3][1] == t[1]:
        right = t[3]
        t[3], right[2] = right[2], t
        right[1] += 1
        return right
    return t


def aa_insert(t, key):
    """Insert as in a plain search tree, then skew and split on the way back up."""
    if t is None:
        return [key, 1, None, None]
    if key < t[0]:
        t[2] = aa_insert(t[2], key)
    elif key > t[0]:
        t[3] = aa_insert(t[3], key)
    return aa_split(aa_skew(t))


def aa_valid(t) -> bool:
    """The AA rules: leaves at level 1; a left child one level down; a right child at most one level down;
    a right grandchild strictly below its grandparent; nodes above level 1 have two children."""
    if t is None:
        return True
    key, lv, l, r = t
    if l is None and r is None and lv != 1:
        return False
    if l and l[1] != lv - 1:
        return False
    if r and not (lv - 1 <= r[1] <= lv):
        return False
    if r and r[3] and r[3][1] >= lv:
        return False
    if lv > 1 and not (l and r):
        return False
    return aa_valid(l) and aa_valid(r)


def aa_height(t) -> int:
    return -1 if t is None else 1 + max(aa_height(t[2]), aa_height(t[3]))


def aa_inorder(t) -> list:
    return [] if t is None else aa_inorder(t[2]) + [t[0]] + aa_inorder(t[3])


if __name__ == "__main__":
    for k in range(1, 8):
        t = RedBlackTree([12, 25, 31, 47, 58, 63, 70][:k])
        print(k, t.shape())
    big = RedBlackTree(range(1000))
    print(big.height(), big.rotations, big.valid())
    import sys
    sys.path.insert(0, "../chapter_18_avl")
    import ch07_examples as avl
    log = []
    avl.build(range(1000), log)
    print("avl rotations", len(log))
