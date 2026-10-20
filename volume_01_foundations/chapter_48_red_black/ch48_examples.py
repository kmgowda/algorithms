"""Volume 1, Chapter 48 - Red-Black Trees.

Run:  python3 ch48_examples.py
"""

from __future__ import annotations

RED, BLACK = "R", "B"


class Node:
    __slots__ = ("key", "colour", "left", "right", "parent")

    def __init__(self, key, colour=RED, parent=None):
        self.key, self.colour, self.left, self.right, self.parent = key, colour, None, None, parent


class RedBlackTree:
    """Insertion with recolouring and rotations (Figures 48.2 and 48.3)."""

    def __init__(self, keys=()):
        self.root = None
        self.rotations = 0
        self.recolours = 0
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
            return a + (n.colour == BLACK)
        try:
            check(self.root)
        except ValueError:
            return False
        return self.root is None or self.root.colour == BLACK


if __name__ == "__main__":
    for k in range(1, 8):
        t = RedBlackTree([12, 25, 31, 47, 58, 63, 70][:k])
        print(k, t.shape())
    big = RedBlackTree(range(1000))
    print(big.height(), big.rotations, big.valid())
    import sys
    sys.path.insert(0, "../chapter_47_avl")
    import ch47_examples as avl
    log = []
    avl.build(range(1000), log)
    print("avl rotations", len(log))
