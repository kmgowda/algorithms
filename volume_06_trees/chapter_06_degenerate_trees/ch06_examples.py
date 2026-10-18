"""Volume 6, Chapter 6 - Why BSTs Go Wrong: Degenerate Trees.

Run:  python3 ch06_examples.py
"""

from __future__ import annotations

import math
import random
from typing import Any


class Node:
    def __init__(self, key: Any) -> None:
        self.key = key
        self.left: Node | None = None
        self.right: Node | None = None


def insert(root: Node | None, key: Any) -> Node:
    """Plain BST insertion (Chapter 5), iterative so tall trees don't hit the recursion limit."""
    if root is None:
        return Node(key)
    node = root
    while True:
        side = "left" if key < node.key else "right"
        child = getattr(node, side)
        if child is None:
            setattr(node, side, Node(key))
            return root
        node = child


def build(keys: list[Any]) -> Node | None:
    root = None
    for k in keys:
        root = insert(root, k)
    return root


def height(root: Node | None) -> int:
    """Iterative height (level-by-level), safe for very tall trees."""
    h, level = -1, [root] if root else []
    while level:
        h += 1
        level = [c for n in level for c in (n.left, n.right) if c]
    return h


def search_steps(root: Node | None, key: Any) -> int:
    """How many nodes a search visits."""
    steps, node = 0, root
    while node is not None:
        steps += 1
        if key == node.key:
            return steps
        node = node.left if key < node.key else node.right
    return steps


def average_depth(root: Node | None) -> float:
    total = count = 0
    level, depth = [root] if root else [], 0
    while level:
        total += depth * len(level)
        count += len(level)
        level = [c for n in level for c in (n.left, n.right) if c]
        depth += 1
    return total / count if count else 0.0


def height_report(n: int, seed: int = 0) -> dict[str, int]:
    """Same n keys, three insertion orders."""
    keys = list(range(n))
    shuffled = keys[:]
    random.Random(seed).shuffle(shuffled)
    return {
        "sorted order": height(build(keys)),
        "reverse order": height(build(keys[::-1])),
        "random order": height(build(shuffled)),
        "best possible": math.floor(math.log2(n)),
    }


def rebuild_balanced(root: Node | None) -> Node | None:
    """A simple cure: read the keys in order and rebuild with the middle key as root (Chapter 5, Exercise 3)."""
    keys: list[Any] = []
    stack, node = [], root
    while stack or node:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        keys.append(node.key)
        node = node.right

    def make(lo: int, hi: int) -> Node | None:
        if lo > hi:
            return None
        mid = (lo + hi) // 2
        n = Node(keys[mid])
        n.left, n.right = make(lo, mid - 1), make(mid + 1, hi)
        return n

    return make(0, len(keys) - 1)


def user_id_index(new_users: int) -> tuple[int, int]:
    """Industry example: user IDs are handed out in increasing order. A plain BST keyed by ID becomes a stick:
    returns (height, steps to find the newest user)."""
    root = build(list(range(1, new_users + 1)))
    return height(root), search_steps(root, new_users)


if __name__ == "__main__":
    print(height_report(1000))
    stick = build(list(range(1, 1001)))
    print("steps to find 1000 in the stick:", search_steps(stick, 1000),
          "| after rebuilding:", search_steps(rebuild_balanced(stick), 1000))
    print("average depth, sorted vs random:", round(average_depth(stick), 1),
          round(average_depth(build(random.Random(1).sample(range(1000), 1000))), 1))
    print("user-ID index (height, steps):", user_id_index(5000))
