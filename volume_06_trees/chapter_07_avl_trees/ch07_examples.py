"""Volume 6, Chapter 7 - AVL Trees: Self-Balancing by Rotation.

Invariant: at every node, the heights of the left and right subtrees differ by at most 1.

Run:  python3 ch07_examples.py
"""

from __future__ import annotations

from typing import Any, Iterator


class Node:
    def __init__(self, key: Any) -> None:
        self.key = key
        self.left: Node | None = None
        self.right: Node | None = None
        self.height = 0                       # a leaf has height 0; an empty tree counts as -1


def h(node: Node | None) -> int:
    return -1 if node is None else node.height


def update(node: Node) -> None:
    node.height = 1 + max(h(node.left), h(node.right))


def balance_factor(node: Node) -> int:
    """left height - right height; AVL allows -1, 0, or +1."""
    return h(node.left) - h(node.right)


def rotate_right(y: Node) -> Node:
    """      y            x
            / \\          / \\
           x   C   ->   A   y
          / \\              / \\
         A   B            B   C        (inorder A x B y C is unchanged)"""
    x = y.left
    assert x is not None
    y.left, x.right = x.right, y
    update(y)
    update(x)
    return x


def rotate_left(x: Node) -> Node:
    """The mirror image of rotate_right."""
    y = x.right
    assert y is not None
    x.right, y.left = y.left, x
    update(x)
    update(y)
    return y


def rebalance(node: Node) -> Node:
    """Fix a node whose balance factor became +2 or -2. Four cases: LL, LR, RR, RL."""
    update(node)
    bf = balance_factor(node)
    if bf > 1:                                   # left side too tall
        assert node.left is not None
        if balance_factor(node.left) < 0:        # left-right case: first rotate the child
            node.left = rotate_left(node.left)
        return rotate_right(node)
    if bf < -1:                                  # right side too tall
        assert node.right is not None
        if balance_factor(node.right) > 0:       # right-left case
            node.right = rotate_right(node.right)
        return rotate_left(node)
    return node


def insert(node: Node | None, key: Any) -> Node:
    """Normal BST insert, then rebalance every node on the way back up."""
    if node is None:
        return Node(key)
    if key < node.key:
        node.left = insert(node.left, key)
    elif key > node.key:
        node.right = insert(node.right, key)
    else:
        return node                              # no duplicates
    return rebalance(node)


def delete(node: Node | None, key: Any) -> Node | None:
    """Normal BST delete (Chapter 5), then rebalance on the way back up."""
    if node is None:
        return None
    if key < node.key:
        node.left = delete(node.left, key)
    elif key > node.key:
        node.right = delete(node.right, key)
    else:
        if node.left is None:
            return node.right
        if node.right is None:
            return node.left
        successor = node.right
        while successor.left is not None:
            successor = successor.left
        node.key = successor.key
        node.right = delete(node.right, successor.key)
    return rebalance(node)


def contains(node: Node | None, key: Any) -> bool:
    while node is not None:
        if key == node.key:
            return True
        node = node.left if key < node.key else node.right
    return False


def inorder(node: Node | None) -> Iterator[Any]:
    if node is not None:
        yield from inorder(node.left)
        yield node.key
        yield from inorder(node.right)


def check(node: Node | None, low: Any = None, high: Any = None) -> int:
    """Verify the BST order, the stored heights, and the AVL balance rule. Returns the height."""
    if node is None:
        return -1
    assert (low is None or node.key > low) and (high is None or node.key < high), "order broken"
    left, right = check(node.left, low, node.key), check(node.right, node.key, high)
    assert abs(left - right) <= 1, "balance broken"
    assert node.height == 1 + max(left, right), "stored height wrong"
    return node.height


def appointments_index(times: list[int]) -> tuple[int, list[int]]:
    """Industry example: a clinic books appointment times in increasing order all day.
    An AVL tree stays short even though the keys arrive sorted. Returns (height, first five times)."""
    root = None
    for t in times:
        root = insert(root, t)
    return h(root), list(inorder(root))[:5]


if __name__ == "__main__":
    root = None
    for k in [10, 20, 30, 40, 50, 25]:
        root = insert(root, k)
    print("inorder:", list(inorder(root)), "| root:", root.key, "| height:", h(root))   # type: ignore[union-attr]
    check(root)
    root = delete(root, 40)
    print("after deleting 40:", list(inorder(root)), "| height:", h(root))
    print("1,000 sorted appointment times -> height", appointments_index(list(range(900, 1900)))[0])
