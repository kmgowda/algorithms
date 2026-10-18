"""Volume 6, Chapter 2 - Binary Trees: Nodes, Children, Height, Depth.

Run:  python3 ch02_examples.py
"""

from __future__ import annotations

from collections import deque
from typing import Any


class Node:
    """A binary tree node: a value and at most two children, left and right."""

    def __init__(self, value: Any, left: "Node | None" = None, right: "Node | None" = None) -> None:
        self.value = value
        self.left = left
        self.right = right


def from_level_list(values: list[Any]) -> Node | None:
    """Build a tree from a level-by-level list where None marks a missing child (LeetCode's format)."""
    if not values or values[0] is None:
        return None
    root = Node(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        for side in ("left", "right"):
            if i < len(values) and values[i] is not None:
                child = Node(values[i])
                setattr(node, side, child)
                queue.append(child)
            i += 1
    return root


def size(node: Node | None) -> int:
    return 0 if node is None else 1 + size(node.left) + size(node.right)


def height(node: Node | None) -> int:
    """Edges on the longest downward path. Empty tree: -1, single node: 0."""
    return -1 if node is None else 1 + max(height(node.left), height(node.right))


def depth_of(node: Node | None, target: Any, depth: int = 0) -> int:
    """Edges from the root down to the first node holding target (-1 if absent)."""
    if node is None:
        return -1
    if node.value == target:
        return depth
    left = depth_of(node.left, target, depth + 1)
    return left if left != -1 else depth_of(node.right, target, depth + 1)


def count_leaves(node: Node | None) -> int:
    if node is None:
        return 0
    if node.left is None and node.right is None:
        return 1
    return count_leaves(node.left) + count_leaves(node.right)


def is_full(node: Node | None) -> bool:
    """Every node has 0 or 2 children."""
    if node is None:
        return True
    if (node.left is None) != (node.right is None):
        return False
    return is_full(node.left) and is_full(node.right)


def is_complete(root: Node | None) -> bool:
    """Every level full except possibly the last, which is filled from the left (the shape of a heap, V5-C7)."""
    queue = deque([root])
    seen_gap = False
    while queue:
        node = queue.popleft()
        if node is None:
            seen_gap = True
        else:
            if seen_gap:
                return False
            queue.append(node.left)
            queue.append(node.right)
    return True


def is_perfect(node: Node | None) -> bool:
    """All leaves at the same depth and every inner node has two children: size == 2^(h+1) - 1."""
    return size(node) == 2 ** (height(node) + 1) - 1


def decide(node: Node, answers: dict[str, bool]) -> Any:
    """Industry example: a yes/no decision tree (left = no, right = yes) - e.g. a simple loan-approval rule."""
    while node.left or node.right:
        node = node.right if answers[node.value] else node.left      # type: ignore[assignment]
    return node.value


if __name__ == "__main__":
    tree = from_level_list(["lion", "tiger", "zebra", "puma", None, "horse", "okapi"])
    print("size", size(tree), "height", height(tree), "leaves", count_leaves(tree), "depth of okapi", depth_of(tree, "okapi"))
    print("full", is_full(tree), "complete", is_complete(tree), "perfect", is_perfect(tree))
    loan = Node("has income?", Node("reject"), Node("good credit?", Node("review by hand"), Node("approve")))
    print(decide(loan, {"has income?": True, "good credit?": False}))
