"""Volume 6, Chapter 4 - Recursive Tree Problems: Height, Diameter, Paths, Lowest Common Ancestor.

Run:  python3 ch04_examples.py
"""

from __future__ import annotations

from typing import Any


class Node:
    def __init__(self, value: Any, left: "Node | None" = None, right: "Node | None" = None) -> None:
        self.value, self.left, self.right = value, left, right


def is_balanced(root: Node | None) -> bool:
    """LeetCode 110: every node's subtrees differ in height by at most 1.
    One pass: check() returns the number of LEVELS (empty tree = 0), or -1 to mean 'unbalanced'."""
    def check(node: Node | None) -> int:
        if node is None:
            return 0
        left, right = check(node.left), check(node.right)
        if left < 0 or right < 0 or abs(left - right) > 1:
            return -1
        return 1 + max(left, right)
    return check(root) >= 0


def diameter(root: Node | None) -> int:
    """LeetCode 543: the longest path (in edges) between ANY two nodes - it may skip the root.

    Each node reports its height upward; while doing so, it checks the path that bends through it.
    """
    best = 0

    def height(node: Node | None) -> int:
        nonlocal best
        if node is None:
            return -1
        left, right = height(node.left), height(node.right)
        best = max(best, left + right + 2)
        return 1 + max(left, right)

    height(root)
    return best


def has_path_sum(node: Node | None, target: int) -> bool:
    """LeetCode 112: is there a root-to-leaf path whose values add up to target?"""
    if node is None:
        return False
    if node.left is None and node.right is None:
        return node.value == target
    rest = target - node.value
    return has_path_sum(node.left, rest) or has_path_sum(node.right, rest)


def all_root_to_leaf_paths(node: Node | None, prefix: tuple = ()) -> list[list]:
    """LeetCode 257: every root-to-leaf path (e.g. every route through a trail system)."""
    if node is None:
        return []
    path = prefix + (node.value,)
    if node.left is None and node.right is None:
        return [list(path)]
    return all_root_to_leaf_paths(node.left, path) + all_root_to_leaf_paths(node.right, path)


def max_path_sum(root: Node) -> int:
    """LeetCode 124: the best total along any path (values may be negative). Same 'bend here' idea as diameter."""
    best = root.value

    def gain(node: Node | None) -> int:
        nonlocal best
        if node is None:
            return 0
        left, right = max(gain(node.left), 0), max(gain(node.right), 0)    # drop branches that only lose
        best = max(best, node.value + left + right)
        return node.value + max(left, right)

    gain(root)
    return best


def lowest_common_ancestor(node: Node | None, a: Any, b: Any) -> Node | None:
    """LeetCode 236: the deepest node that has both a and b below it (or is one of them).

    Industry example: the closest shared manager of two employees, or the shared folder of two files.
    """
    if node is None or node.value in (a, b):
        return node
    left = lowest_common_ancestor(node.left, a, b)
    right = lowest_common_ancestor(node.right, a, b)
    if left and right:
        return node                      # a on one side, b on the other: this is where they meet
    return left or right


if __name__ == "__main__":
    org = Node("CEO", Node("CTO", Node("Dev Lead", Node("Ana"), Node("Ben")), Node("QA Lead")),
               Node("CFO", None, Node("Accountant")))
    print("balanced?", is_balanced(org), "| diameter:", diameter(org))
    print("shared manager of Ana and QA Lead:", lowest_common_ancestor(org, "Ana", "QA Lead").value)  # type: ignore[union-attr]
    trails = Node(5, Node(4, Node(11, Node(7), Node(2))), Node(8, Node(13), Node(4, None, Node(1))))
    print("path summing to 22?", has_path_sum(trails, 22), all_root_to_leaf_paths(trails))
    print("best path sum:", max_path_sum(Node(-10, Node(9), Node(20, Node(15), Node(7)))))
