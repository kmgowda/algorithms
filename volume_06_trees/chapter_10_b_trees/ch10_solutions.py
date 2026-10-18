"""Volume 6, Chapter 10 - Solutions to the exercises."""

from __future__ import annotations

import math

from ch10_examples import BTree


def max_keys(t: int, height: int) -> int:
    """Exercise 1: a full B-tree of height h holds (2t)^(h+1) - 1 keys."""
    return (2 * t) ** (height + 1) - 1


def max_height(n: int, t: int) -> int:
    """Exercise 2: a B-tree with n keys has height at most log_t((n + 1) / 2)."""
    return math.floor(math.log((n + 1) / 2, t)) if n > 1 else 0


def count_nodes(tree: BTree) -> int:
    """Exercise 3: how many nodes (disk pages) does the tree use?"""
    total, stack = 0, [tree.root]
    while stack:
        node = stack.pop()
        total += 1
        stack.extend(node.children)
    return total


def minimum_key(tree: BTree):
    """Exercise 4: follow the leftmost children down to a leaf."""
    node = tree.root
    while not node.leaf:
        node = node.children[0]
    return node.keys[0] if node.keys else None


if __name__ == "__main__":
    tr = BTree(2)
    for k in [10, 20, 5, 6, 12, 30, 7, 17]:
        tr.insert(k)
    print(max_keys(2, 2), max_height(10**6, 100), count_nodes(tr), minimum_key(tr))
