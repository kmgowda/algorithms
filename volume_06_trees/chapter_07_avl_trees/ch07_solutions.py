"""Volume 6, Chapter 7 - Solutions to the exercises."""

from __future__ import annotations

import ch07_examples as avl
from ch07_examples import Node, h, insert


def rotations_used(keys: list[int]) -> int:
    """Exercise 1: count rotations while inserting keys, by temporarily wrapping the rotation functions."""
    count = 0
    original_left, original_right = avl.rotate_left, avl.rotate_right

    def counting_left(x: Node) -> Node:
        nonlocal count
        count += 1
        return original_left(x)

    def counting_right(y: Node) -> Node:
        nonlocal count
        count += 1
        return original_right(y)

    avl.rotate_left, avl.rotate_right = counting_left, counting_right
    try:
        root = None
        for k in keys:
            root = insert(root, k)
    finally:
        avl.rotate_left, avl.rotate_right = original_left, original_right
    return count


def min_nodes_for_height(height: int) -> int:
    """Exercise 2: the sparsest AVL tree of height h has N(h) = N(h-1) + N(h-2) + 1 nodes (a Fibonacci-like
    recurrence), so height grows at most about 1.44 log2 n."""
    if height < 0:
        return 0
    if height == 0:
        return 1
    a, b = 1, 2                                      # N(0), N(1)
    for _ in range(height - 1):
        a, b = b, a + b + 1
    return b


def max_avl_height(n: int) -> int:
    """Exercise 3: the tallest an AVL tree with n nodes can be."""
    height = 0
    while min_nodes_for_height(height + 1) <= n:
        height += 1
    return height


def build_from_keys(keys: list[int]) -> int:
    """Exercise 4: the AVL height after inserting keys (for comparing with a plain BST)."""
    root = None
    for k in keys:
        root = insert(root, k)
    return h(root)


if __name__ == "__main__":
    print(rotations_used([1, 2, 3]), [min_nodes_for_height(x) for x in range(6)], max_avl_height(1000), build_from_keys(list(range(1000))))
