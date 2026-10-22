"""Volume 3, Chapter 4 - Recursive Tree Problems.

Run:  python3 ch04_examples.py
"""

from __future__ import annotations

import math


class Node:
    def __init__(self, value, left=None, right=None):
        self.value, self.left, self.right = value, left, right


def library() -> Node:
    """Chapter 4's sections, with the books shelved directly in each (Figure 4.1)."""
    maths = Node(6, Node(12), Node(9))
    return Node(2, Node(5, Node(30), Node(22)), Node(4, Node(18), maths))


def size(n) -> int:
    return 0 if n is None else 1 + size(n.left) + size(n.right)


def total(n) -> int:
    """Base case, ask each child, combine (Section 4.4)."""
    if n is None:
        return 0
    return n.value + total(n.left) + total(n.right)


def height(n) -> int:
    return -1 if n is None else 1 + max(height(n.left), height(n.right))


def largest(n) -> float:
    return -math.inf if n is None else max(n.value, largest(n.left), largest(n.right))


def mirror(n):
    """Swap left and right everywhere, returning a new tree (Figure 4.3)."""
    return None if n is None else Node(n.value, mirror(n.right), mirror(n.left))


def same_tree(a, b) -> bool:
    """Two trees are identical if both are empty, or roots, left subtrees and right subtrees all match."""
    if a is None or b is None:
        return a is b
    return a.value == b.value and same_tree(a.left, b.left) and same_tree(a.right, b.right)


def symmetric(n) -> bool:
    return same_tree(n, mirror(n))


def best_walk(n) -> int:
    """Most books on a root-to-leaf walk (Figure 4.4)."""
    kids = [c for c in (n.left, n.right) if c is not None]
    return n.value if not kids else n.value + max(best_walk(c) for c in kids)


def min_depth(n) -> int:
    """Fewest edges from the root down to a leaf (Section 4.4). A missing child is not a leaf, so a node with one
    child must use the other side; min(left, right) + 1 would wrongly stop at the empty side."""
    if n is None:
        return -1
    if n.left is None and n.right is None:
        return 0
    kids = [c for c in (n.left, n.right) if c is not None]
    return 1 + min(min_depth(c) for c in kids)


def lowest_common_ancestor(n, a, b):
    """The deepest node with both a and b in its subtree (Section 4.5); None if either value is missing.
    Each call reports how many of a and b its subtree holds; the first node to see both is the answer."""
    found = None

    def count(node) -> int:
        nonlocal found
        if node is None:
            return 0
        c = count(node.left) + count(node.right) + (node.value == a) + (node.value == b)
        if c >= 2 and found is None:
            found = node
        return c
    count(n)
    return found


def paths_with_total(n, target, so_far=0) -> int:
    """Section 4.15: carry the running total down; count the root-to-leaf paths whose total is target."""
    if n is None:
        return 0
    so_far += n.value
    if n.left is None and n.right is None:
        return 1 if so_far == target else 0
    return paths_with_total(n.left, target, so_far) + paths_with_total(n.right, target, so_far)


if __name__ == "__main__":
    lib = library()
    print(size(lib), total(lib), height(lib), largest(lib), best_walk(lib))
    print(min_depth(lib), lowest_common_ancestor(lib, 12, 18).value)
    print(same_tree(lib, mirror(mirror(lib))), symmetric(Node(1, Node(2, Node(3), Node(4)), Node(2, Node(4), Node(3)))))
