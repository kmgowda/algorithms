"""Volume 2, Chapter 18 - AVL Trees.

Run:  python3 ch18_examples.py
"""

from __future__ import annotations

import random


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


def rebalance(n, log=None):
    """Update n's height and repair a balance factor of +2 or -2 (Figures 18.3 and 18.4).
    Shared by insert and delete; the four cases are named by where the tall side is."""
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


def insert(n, key, log=None):
    """Insert as in a plain BST, then rebalance on the way back up (Figures 18.3 and 18.5)."""
    if n is None:
        return Node(key)
    if key < n.key:
        n.left = insert(n.left, key, log)
    elif key > n.key:
        n.right = insert(n.right, key, log)
    else:
        return n
    return rebalance(n, log)


def delete(n, key, log=None):
    """Delete as in a plain BST (Chapter 16), then rebalance every node on the way back up (Figure 18.6).
    A missing key leaves the tree unchanged. Returns the new root of this subtree."""
    if n is None:
        return None
    if key < n.key:
        n.left = delete(n.left, key, log)
    elif key > n.key:
        n.right = delete(n.right, key, log)
    else:
        if n.left is None or n.right is None:   # zero or one child: splice the node out
            return n.left or n.right
        s = n.right                             # two children: copy the successor, delete it below
        while s.left is not None:
            s = s.left
        n.key = s.key
        n.right = delete(n.right, s.key, log)
    return rebalance(n, log)


def delete_all(root, keys, log=None):
    for k in keys:
        root = delete(root, k, log)
    return root


def sparsest(height: int, start: int = 10, step: int = 10):
    """The sparsest AVL tree of a height (fewest_nodes(height) nodes): its left subtree is a sparsest tree one level
    shorter than its right. Keys start, start + step, ... in order (Figures 18.6 and 18.7)."""
    keys = iter(range(start, start + step * fewest_nodes(height), step))

    def make(hh):
        if hh < 0:
            return None
        left = make(hh - 2)
        n = Node(next(keys))
        n.left, n.right = left, make(hh - 1)
        update(n)
        return n
    return make(height)


def cascade(height: int) -> int:
    """Repairs needed to delete the smallest key of the sparsest AVL tree of a height (Challenge 18.1)."""
    log = []
    delete(sparsest(height), 10, log)
    return len(log)


def random_deletions(n: int = 10_000, seed: int = 1):
    """Build a tree from n random keys, delete them all in random order: (repairs, most in one deletion,
    rotations counting a double rotation as two) (Section 18.8)."""
    rng = random.Random(seed)
    keys = rng.sample(range(10 ** 6), n)
    t = build(keys)
    order = keys[:]
    rng.shuffle(order)
    total = most = rotations = 0
    for k in order:
        log = []
        t = delete(t, k, log)
        total += len(log)
        most = max(most, len(log))
        rotations += sum(2 if c in ("LR", "RL") else 1 for c, _ in log)
    return total, most, rotations


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
    """Every balance factor in -1..+1 and every stored height correct."""
    if n is None:
        return True
    ok = n.height == 1 + max(h(n.left), h(n.right))
    return ok and abs(balance(n)) <= 1 and is_avl(n.left) and is_avl(n.right)


def fewest_nodes(height: int) -> int:
    """N(h) = 1 + N(h - 1) + N(h - 2), N(0) = 1, N(1) = 2: the sparsest AVL tree of each height (Figure 18.7)."""
    a, b = 1, 2
    if height == 0:
        return 1
    for _ in range(height - 1):
        a, b = b, 1 + a + b
    return b


if __name__ == "__main__":
    log = []
    t = build([12, 25, 31, 47, 58, 63, 70], log)
    print(shape(t), t.height, log)
    big = build(range(1000))
    print(big.height, is_avl(big))
    print(shape(build([47, 25, 12])), shape(build([47, 25, 31])))
