"""Volume 1, Chapter 44 - Recursive Tree Problems.

Run:  python3 ch44_examples.py
"""

from __future__ import annotations

import math


class Node:
    def __init__(self, value, left=None, right=None):
        self.value, self.left, self.right = value, left, right


def library() -> Node:
    """Chapter 44's sections, with the books shelved directly in each (Figure 44.1)."""
    maths = Node(6, Node(12), Node(9))
    return Node(2, Node(5, Node(30), Node(22)), Node(4, Node(18), maths))


def size(n) -> int:
    return 0 if n is None else 1 + size(n.left) + size(n.right)


def total(n) -> int:
    """Base case, ask each child, combine (Section 44.4)."""
    if n is None:
        return 0
    return n.value + total(n.left) + total(n.right)


def height(n) -> int:
    return -1 if n is None else 1 + max(height(n.left), height(n.right))


def largest(n) -> float:
    return -math.inf if n is None else max(n.value, largest(n.left), largest(n.right))


def mirror(n):
    """Swap left and right everywhere, returning a new tree (Figure 44.3)."""
    return None if n is None else Node(n.value, mirror(n.right), mirror(n.left))


def same_tree(a, b) -> bool:
    """Two trees are identical if both are empty, or roots, left subtrees and right subtrees all match."""
    if a is None or b is None:
        return a is b
    return a.value == b.value and same_tree(a.left, b.left) and same_tree(a.right, b.right)


def symmetric(n) -> bool:
    return same_tree(n, mirror(n))


def best_walk(n) -> int:
    """Most books on a root-to-leaf walk (Figure 44.4)."""
    kids = [c for c in (n.left, n.right) if c is not None]
    return n.value if not kids else n.value + max(best_walk(c) for c in kids)


if __name__ == "__main__":
    lib = library()
    print(size(lib), total(lib), height(lib), largest(lib), best_walk(lib))
    print(same_tree(lib, mirror(mirror(lib))), symmetric(Node(1, Node(2, Node(3), Node(4)), Node(2, Node(4), Node(3)))))
