"""Volume 6, Chapter 12 - Solutions to the exercises."""

from __future__ import annotations

from collections import deque
from typing import Any

from ch12_examples import Node


def build_from_post_in(postorder: list[Any], inorder: list[Any]) -> Node | None:
    """Exercise 1 (LeetCode 106): postorder's LAST value is the root; build right before left."""
    position = {v: i for i, v in enumerate(inorder)}
    post = list(postorder)

    def build(lo: int, hi: int) -> Node | None:
        if lo > hi:
            return None
        value = post.pop()
        node = Node(value)
        mid = position[value]
        node.right = build(mid + 1, hi)
        node.left = build(lo, mid - 1)
        return node

    return build(0, len(inorder) - 1)


def serialize_levels(root: Node | None) -> list[Any]:
    """Exercise 2: LeetCode's level-order format with None for gaps, trailing Nones removed."""
    out: list[Any] = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            out.append(None)
            continue
        out.append(node.value)
        queue.append(node.left)
        queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


def left_view(root: Node | None) -> list[Any]:
    """Exercise 3: the first node on each level."""
    view, level = [], [root] if root else []
    while level:
        view.append(level[0].value)
        level = [c for n in level for c in (n.left, n.right) if c]
    return view


def bst_from_preorder(preorder: list[int]) -> Node | None:
    """Exercise 4 (LeetCode 1008): a BST's preorder alone is enough - values give the shape. O(n) with bounds."""
    it = iter(preorder)
    nxt = [next(it, None)]

    def build(high: float) -> Node | None:
        if nxt[0] is None or nxt[0] > high:
            return None
        node = Node(nxt[0])
        nxt[0] = next(it, None)
        node.left = build(node.value)
        node.right = build(high)
        return node

    return build(float("inf"))


if __name__ == "__main__":
    from ch12_examples import serialize
    print(serialize(build_from_post_in([9, 15, 7, 20, 3], [9, 3, 15, 20, 7])))
    t = Node(1, Node(2, None, Node(4)), Node(3))
    print(serialize_levels(t), left_view(t), serialize(bst_from_preorder([8, 5, 1, 7, 10, 12])))
