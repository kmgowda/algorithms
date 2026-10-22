"""Volume 3, Chapter 8 - Red-Black Trees: companion code for the Thinking Problems (Section 8.16).

Run:  python3 ch08_solutions.py
"""

from __future__ import annotations

import os
import sys

from ch08_examples import BLACK, RED, Node, RedBlackTree, colour

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "chapter_07_avl"))
import ch07_examples as avl  # noqa: E402


def colour_avl(root) -> RedBlackTree:
    """Thinking Problem 1: copy an AVL tree (Chapter 7 nodes) and colour it as a valid red-black tree.
    A subtree of height h is painted black-rooted with black height (h + 2) // 2, or, when h is even,
    red-rooted with black height h // 2; each child gets whichever painting gives the black height needed."""
    t = RedBlackTree()

    def paint(a, parent, need):                  # need: the black height this subtree must have
        if a is None:
            return None
        hh = a.height
        red = (hh + 2) // 2 != need               # a black root would give too much: paint it red
        n = Node(a.key, RED if red else BLACK, parent)
        below = need if red else need - 1
        n.left, n.right = paint(a.left, n, below), paint(a.right, n, below)
        return n
    t.root = paint(root, None, (avl.h(root) + 2) // 2)
    return t


def rb_from_sorted(keys) -> RedBlackTree:
    """Thinking Problem 2: a valid red-black tree from sorted distinct keys in O(n). Middle key at the root
    (Chapter 11); if the tree is not perfect, its deepest level is painted red and every other node black."""
    n = len(keys)
    deepest = n.bit_length() - 1                  # the height of the middle-split tree
    perfect = n == 2 ** (deepest + 1) - 1
    t = RedBlackTree()

    def build(lo, hi, depth, parent):
        if lo > hi:
            return None
        mid = (lo + hi) // 2
        node = Node(keys[mid], RED if depth == deepest and not perfect else BLACK, parent)
        node.left = build(lo, mid - 1, depth + 1, node)
        node.right = build(mid + 1, hi, depth + 1, node)
        return node
    t.root = build(0, n - 1, 0, None)
    return t


class SkipCase3Tree(RedBlackTree):
    """Thinking Problem 3: a deletion repair that goes straight to case 4 whenever the sibling has any red
    child, skipping case 3. Wrong when only the near child is red."""

    def _fix_delete(self, x, parent):
        while x is not self.root and colour(x) == BLACK:
            left = x is parent.left
            w = parent.right if left else parent.left
            if w.colour == RED:                                # case 1
                w.colour, parent.colour = BLACK, RED
                self._rotate_left(parent) if left else self._rotate_right(parent)
                self.cases.append(1)
                w = parent.right if left else parent.left
            near, far = (w.left, w.right) if left else (w.right, w.left)
            if colour(near) == BLACK and colour(far) == BLACK:  # case 2
                w.colour = RED
                self.cases.append(2)
                x, parent = parent, parent.parent
                continue
            w.colour, parent.colour = parent.colour, BLACK      # "case 4" at once, even if far is empty
            if far is not None:
                far.colour = BLACK
            self._rotate_left(parent) if left else self._rotate_right(parent)
            self.cases.append(4)
            x = self.root
        if x is not None:
            x.colour = BLACK


if __name__ == "__main__":
    t = colour_avl(avl.sparsest(4))
    print(t.shape(), t.valid())
    print(rb_from_sorted([12, 25, 31, 47, 58, 63, 70, 84, 91]).shape())
    bad = SkipCase3Tree([12, 25, 31, 47, 58, 63, 70])
    bad.delete(70)
    bad.delete(31)
    print(bad.shape(), bad.valid())
