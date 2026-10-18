"""Volume 6, Chapter 3 - Tree Traversals: Preorder, Inorder, Postorder, Level Order.

Run:  python3 ch03_examples.py
"""

from __future__ import annotations

from collections import deque
from typing import Any


class Node:
    def __init__(self, value: Any, left: "Node | None" = None, right: "Node | None" = None) -> None:
        self.value, self.left, self.right = value, left, right


def preorder(node: Node | None) -> list:
    """Node, then left subtree, then right subtree - 'visit before children' (like a table of contents)."""
    return [] if node is None else [node.value] + preorder(node.left) + preorder(node.right)


def inorder(node: Node | None) -> list:
    """Left subtree, node, right subtree - on a binary search tree this gives SORTED order (Chapter 5)."""
    return [] if node is None else inorder(node.left) + [node.value] + inorder(node.right)


def postorder(node: Node | None) -> list:
    """Left, right, then node - 'children before parent' (evaluate, delete, total up)."""
    return [] if node is None else postorder(node.left) + postorder(node.right) + [node.value]


def level_order(root: Node | None) -> list[list]:
    """Level by level with a queue (LeetCode 102)."""
    if root is None:
        return []
    levels, queue = [], deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.value)
            queue.extend(child for child in (node.left, node.right) if child is not None)
        levels.append(level)
    return levels


def inorder_iterative(root: Node | None) -> list:
    """Inorder with an explicit stack (V2-C8): go left as far as possible, visit, then go right."""
    out, stack, node = [], [], root
    while stack or node is not None:
        while node is not None:
            stack.append(node)
            node = node.left
        node = stack.pop()
        out.append(node.value)
        node = node.right
    return out


def preorder_iterative(root: Node | None) -> list:
    """Preorder with a stack: push right before left so left is visited first."""
    out, stack = [], [root] if root else []
    while stack:
        node = stack.pop()
        out.append(node.value)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return out


def evaluate(node: Node) -> float:
    """Industry example: an expression tree is evaluated in POSTORDER - both operands before the operator."""
    if node.left is None and node.right is None:
        return float(node.value)
    a, b = evaluate(node.left), evaluate(node.right)        # type: ignore[arg-type]
    return {"+": a + b, "-": a - b, "*": a * b, "/": a / b}[node.value]


def table_of_contents(node: Node | None, depth: int = 0) -> list[str]:
    """Practical example: a book outline printed in PREORDER with indentation."""
    if node is None:
        return []
    return ["  " * depth + str(node.value)] + table_of_contents(node.left, depth + 1) + table_of_contents(node.right, depth + 1)


if __name__ == "__main__":
    #        F
    #      /   \
    #     B     G
    #    / \     \
    #   A   D     I
    #      / \   /
    #     C   E H
    tree = Node("F", Node("B", Node("A"), Node("D", Node("C"), Node("E"))), Node("G", None, Node("I", Node("H"))))
    print("pre ", preorder(tree))
    print("in  ", inorder(tree), inorder_iterative(tree) == inorder(tree))
    print("post", postorder(tree))
    print("levels", level_order(tree))
    expr = Node("*", Node("+", Node(2), Node(3)), Node(4))
    print("(2 + 3) * 4 =", evaluate(expr), "| postfix:", postorder(expr))
    book = Node("Zoo Guide", Node("Mammals", Node("Lions"), Node("Zebras")), Node("Birds", Node("Eagles")))
    print("\n".join(table_of_contents(book)))
