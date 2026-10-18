"""Volume 6, Chapter 12 - Serialization, Construction, and Tree Views.

Run:  python3 ch12_examples.py
"""

from __future__ import annotations

from collections import deque
from typing import Any


class Node:
    def __init__(self, value: Any, left: "Node | None" = None, right: "Node | None" = None) -> None:
        self.value, self.left, self.right = value, left, right


def serialize(root: Node | None) -> str:
    """LeetCode 297: preorder with '#' for empty children, comma separated. Saves the exact shape."""
    out: list[str] = []

    def walk(node: Node | None) -> None:
        if node is None:
            out.append("#")
            return
        out.append(str(node.value))
        walk(node.left)
        walk(node.right)

    walk(root)
    return ",".join(out)


def deserialize(text: str) -> Node | None:
    """Read the tokens back in the same preorder; '#' means 'no child here'."""
    tokens = iter(text.split(","))

    def build() -> Node | None:
        token = next(tokens)
        if token == "#":
            return None
        node = Node(int(token) if token.lstrip("-").isdigit() else token)
        node.left = build()
        node.right = build()
        return node

    return build()


def build_from_pre_in(preorder: list[Any], inorder: list[Any]) -> Node | None:
    """LeetCode 105: preorder's first value is the root; its position in inorder splits left from right.
    Distinct values required. O(n) with a position dictionary."""
    position = {v: i for i, v in enumerate(inorder)}
    pre = iter(preorder)

    def build(lo: int, hi: int) -> Node | None:
        if lo > hi:
            return None
        value = next(pre)
        node = Node(value)
        mid = position[value]
        node.left = build(lo, mid - 1)
        node.right = build(mid + 1, hi)
        return node

    return build(0, len(inorder) - 1)


def vertical_columns(root: Node | None) -> list[list[Any]]:
    """LeetCode 314 idea: column 0 at the root, left child -1, right child +1; top-to-bottom within a column."""
    columns: dict[int, list[Any]] = {}
    queue = deque([(root, 0)] if root else [])
    while queue:
        node, col = queue.popleft()
        columns.setdefault(col, []).append(node.value)
        if node.left:
            queue.append((node.left, col - 1))
        if node.right:
            queue.append((node.right, col + 1))
    return [columns[c] for c in sorted(columns)]


def top_view(root: Node | None) -> list[Any]:
    """What you see looking down from above: the first (highest) node in each column."""
    return [col[0] for col in vertical_columns(root)]


def bottom_view(root: Node | None) -> list[Any]:
    """Looking up from below: the last (lowest) node in each column."""
    return [col[-1] for col in vertical_columns(root)]


def same_tree(a: Node | None, b: Node | None) -> bool:
    if a is None or b is None:
        return a is b
    return a.value == b.value and same_tree(a.left, b.left) and same_tree(a.right, b.right)


if __name__ == "__main__":
    family = Node("Grandma", Node("Mum", Node("Ana"), Node("Ben")), Node("Uncle", None, Node("Cy")))
    text = serialize(family)
    print(text)
    print("round trip equal:", same_tree(family, deserialize(text)))
    t = build_from_pre_in([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])
    print("rebuilt:", serialize(t))
    print("columns:", vertical_columns(family), "| top:", top_view(family), "| bottom:", bottom_view(family))
