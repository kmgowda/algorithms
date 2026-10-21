"""Volume 2, Chapter 18 - AVL Trees.

Run:  python3 ch18_examples.py
"""

from __future__ import annotations


class Node:
    __slots__ = ("key", "left", "right", "height")

    def __init__(self, key):
        self.key, self.left, self.right, self.height = key, None, None, 0


def h(n) -> int:
    return -1 if n is None else n.height


def update(n) -> None:
    n.height = 1 + max(h(n.left), h(n.right))


def balance(n) -> int:
    """Balance factor: height of the left subtree minus height of the right (Figure 18.1)."""
    return h(n.left) - h(n.right)


def rotate_right(y):
    """Lift y's left child x above y (Figure 18.2)."""
    x = y.left
    y.left, x.right = x.right, y
    update(y)
    update(x)
    return x


def rotate_left(x):
    y = x.right
    x.right, y.left = y.left, x
    update(x)
    update(y)
    return y


def insert(n, key, log=None):
    """Insert as in a plain BST, then rebalance on the way back up (Figures 18.3 and 18.4)."""
    if n is None:
        return Node(key)
    if key < n.key:
        n.left = insert(n.left, key, log)
    elif key > n.key:
        n.right = insert(n.right, key, log)
    else:
        return n
    update(n)
    b = balance(n)
    if b > 1:                                   # left side too tall
        if balance(n.left) < 0:                 # left-right case: first straighten
            n.left = rotate_left(n.left)
            log is not None and log.append(("LR", n.key))
        else:
            log is not None and log.append(("LL", n.key))
        return rotate_right(n)
    if b < -1:                                  # right side too tall
        if balance(n.right) > 0:                # right-left case
            n.right = rotate_right(n.right)
            log is not None and log.append(("RL", n.key))
        else:
            log is not None and log.append(("RR", n.key))
        return rotate_left(n)
    return n


def build(keys, log=None):
    root = None
    for k in keys:
        root = insert(root, k, log)
    return root


def inorder(n) -> list:
    return [] if n is None else inorder(n.left) + [n.key] + inorder(n.right)


def shape(n):
    """(key, left shape, right shape) for drawing and testing."""
    return None if n is None else (n.key, shape(n.left), shape(n.right))


def is_avl(n) -> bool:
    if n is None:
        return True
    return abs(balance(n)) <= 1 and is_avl(n.left) and is_avl(n.right)


if __name__ == "__main__":
    log = []
    t = build([12, 25, 31, 47, 58, 63, 70], log)
    print(shape(t), t.height, log)
    big = build(range(1000))
    print(big.height, is_avl(big))
    print(shape(build([47, 25, 12])), shape(build([47, 25, 31])))
