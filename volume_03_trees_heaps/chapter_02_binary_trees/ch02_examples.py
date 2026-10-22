"""Volume 3, Chapter 2 - Binary Trees.

Run:  python3 ch02_examples.py
"""

from __future__ import annotations

import operator


class TreeNode:
    """A binary-tree node: a value and links to left and right children (Figure 2.2)."""

    def __init__(self, value, left=None, right=None):
        self.value, self.left, self.right = value, left, right


def from_array(values: list, i: int = 0):
    """Build linked nodes from a complete tree stored in an array (Figure 2.4)."""
    if i >= len(values):
        return None
    return TreeNode(values[i], from_array(values, 2 * i + 1), from_array(values, 2 * i + 2))


def children_of(i: int) -> tuple[int, int]:
    return 2 * i + 1, 2 * i + 2


def parent_of(i: int) -> int:
    return (i - 1) // 2


def count(node) -> int:
    return 0 if node is None else 1 + count(node.left) + count(node.right)


def height(node) -> int:
    """Edges on the longest root-to-leaf path; an empty tree has height -1."""
    return -1 if node is None else 1 + max(height(node.left), height(node.right))


OPS = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}


def evaluate(node):
    """Section 2.8: a leaf is a number; an operator applies to its two subtrees' values."""
    if node.left is None and node.right is None:
        return node.value
    return OPS[node.value](evaluate(node.left), evaluate(node.right))


def postfix(node) -> list:
    if node is None:
        return []
    return postfix(node.left) + postfix(node.right) + [node.value]


if __name__ == "__main__":
    root = from_array([58, 25, 84, 12, 47, 70, 91, 9])
    print(count(root), height(root), children_of(1), children_of(2), parent_of(7))
    expr = TreeNode("*", TreeNode("+", TreeNode(3), TreeNode(4)), TreeNode(2))
    print(evaluate(expr), postfix(expr))
    print(evaluate(TreeNode("-", TreeNode(5), TreeNode("+", TreeNode(2), TreeNode(1)))))
