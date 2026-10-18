"""Volume 6, Chapter 8 - Solutions to the exercises."""

from __future__ import annotations

import math

from ch08_examples import Node, RedBlackTree, is_red


def count_red(node: Node | None) -> int:
    """Exercise 1: how many red nodes (= red links) are in the tree?"""
    if node is None:
        return 0
    return (1 if is_red(node) else 0) + count_red(node.left) + count_red(node.right)


def as_23_tree_nodes(node: Node | None) -> int:
    """Exercise 2: a left-leaning red-black tree IS a 2-3 tree: a black node with a red left child
    is one 3-node. The number of 2-3 nodes = black nodes."""
    if node is None:
        return 0
    return (0 if is_red(node) else 1) + as_23_tree_nodes(node.left) + as_23_tree_nodes(node.right)


def height_bound(n: int) -> float:
    """Exercise 3: a red-black tree's height is at most 2 * log2(n + 1)."""
    return 2 * math.log2(n + 1)


def floor_key(tree: RedBlackTree, key):
    """Exercise 4: floor works exactly as in a plain BST (Chapter 5) - colors don't affect searching."""
    node, best = tree.root, None
    while node is not None:
        if node.key == key:
            return key
        if node.key < key:
            best, node = node.key, node.right
        else:
            node = node.left
    return best


if __name__ == "__main__":
    t = RedBlackTree()
    for k in range(1, 16):
        t.insert(k)
    print(count_red(t.root), as_23_tree_nodes(t.root), round(height_bound(15), 2), floor_key(t, 7.5))
