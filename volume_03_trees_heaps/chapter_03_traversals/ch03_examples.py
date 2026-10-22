"""Volume 3, Chapter 3 - Tree Traversals.

Run:  python3 ch03_examples.py
"""

from __future__ import annotations

from collections import deque


class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value, self.left, self.right = value, left, right


def from_array(values: list, i: int = 0):
    if i >= len(values):
        return None
    return TreeNode(values[i], from_array(values, 2 * i + 1), from_array(values, 2 * i + 2))


def preorder(n):
    return [] if n is None else [n.value] + preorder(n.left) + preorder(n.right)


def inorder(n):
    return [] if n is None else inorder(n.left) + [n.value] + inorder(n.right)


def postorder(n):
    return [] if n is None else postorder(n.left) + postorder(n.right) + [n.value]


def level_order(root) -> list:
    """Row by row with a queue (Section 3.6)."""
    out, q = [], deque([root] if root else [])
    while q:
        n = q.popleft()
        out.append(n.value)
        for c in (n.left, n.right):
            if c:
                q.append(c)
    return out


def levels(root) -> list[list]:
    """Level by level (Section 3.6): the queue's length at the start of a round is the size of one level."""
    out, q = [], deque([root] if root else [])
    while q:
        row = []
        for _ in range(len(q)):
            n = q.popleft()
            row.append(n.value)
            for c in (n.left, n.right):
                if c:
                    q.append(c)
        out.append(row)
    return out


def inorder_iterative(root) -> list:
    """Inorder with an explicit stack: safe for very deep trees."""
    out, stack, n = [], [], root
    while stack or n:
        while n:
            stack.append(n)
            n = n.left
        n = stack.pop()
        out.append(n.value)
        n = n.right
    return out


def folder_totals(own: dict[str, int], children: dict[str, list[str]], root: str) -> dict[str, int]:
    """Section 3.9: postorder - children's totals first, then the folder."""
    totals: dict[str, int] = {}

    def visit(f):
        totals[f] = own[f] + sum(visit(c) for c in children.get(f, []))
        return totals[f]
    visit(root)
    return totals


if __name__ == "__main__":
    t = from_array([58, 25, 84, 12, 47, 70, 91])
    print(preorder(t), inorder(t), postorder(t), level_order(t), inorder_iterative(t))
    print(levels(t))
    print(folder_totals({"Home": 1, "Docs": 3, "Photos": 10, "Old": 2},
                        {"Home": ["Docs", "Photos"], "Docs": ["Old"]}, "Home"))
