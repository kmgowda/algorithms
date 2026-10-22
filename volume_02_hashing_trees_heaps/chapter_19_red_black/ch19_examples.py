"""Volume 2, Chapter 19 - Red-Black Trees.

Run:  python3 ch19_examples.py
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
    """Insertion with recolouring and rotations (Figures 19.3 and 19.4), deletion with the four sibling cases
    (Figures 19.5 and 19.6). `cases` logs the repairs of the most recent delete."""

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
        """x (possibly empty) carries an extra black; parent is its parent (Figure 19.6)."""
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
        """Black nodes on any path from n down to an empty spot, counting n itself if it is black (Figure 19.2)."""
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
    how often each repair case ran) (Section 19.6)."""
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


if __name__ == "__main__":
    for k in range(1, 8):
        t = RedBlackTree([12, 25, 31, 47, 58, 63, 70][:k])
        print(k, t.shape())
    big = RedBlackTree(range(1000))
    print(big.height(), big.rotations, big.valid())
    import sys
    sys.path.insert(0, "../chapter_18_avl")
    import ch18_examples as avl
    log = []
    avl.build(range(1000), log)
    print("avl rotations", len(log))
