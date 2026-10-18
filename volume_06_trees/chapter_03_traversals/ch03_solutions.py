"""Volume 6, Chapter 3 - Solutions to the exercises."""

from __future__ import annotations

from collections import deque

from ch03_examples import Node


def postorder_iterative(root: Node | None) -> list:
    """Exercise 1: reverse of a 'node, right, left' preorder is a postorder."""
    out, stack = [], [root] if root else []
    while stack:
        node = stack.pop()
        out.append(node.value)
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
    return out[::-1]


def zigzag_levels(root: Node | None) -> list[list]:
    """Exercise 2 (LeetCode 103): level order, alternating left-to-right and right-to-left."""
    levels, queue, flip = [], deque([root] if root else []), False
    while queue:
        level = [n.value for n in queue]
        levels.append(level[::-1] if flip else level)
        flip = not flip
        queue = deque(c for n in queue for c in (n.left, n.right) if c)
    return levels


def right_side_view(root: Node | None) -> list:
    """Exercise 3 (LeetCode 199): the last node of each level."""
    view, queue = [], deque([root] if root else [])
    while queue:
        view.append(queue[-1].value)
        queue = deque(c for n in queue for c in (n.left, n.right) if c)
    return view


def level_averages(root: Node | None) -> list[float]:
    """Exercise 4 (LeetCode 637): average value per level (e.g. average age per generation)."""
    out, queue = [], deque([root] if root else [])
    while queue:
        out.append(sum(n.value for n in queue) / len(queue))
        queue = deque(c for n in queue for c in (n.left, n.right) if c)
    return out


if __name__ == "__main__":
    t = Node(3, Node(9), Node(20, Node(15), Node(7)))
    print(postorder_iterative(t), zigzag_levels(t), right_side_view(t), level_averages(t))
