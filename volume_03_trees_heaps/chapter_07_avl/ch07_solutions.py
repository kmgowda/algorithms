"""Volume 3, Chapter 7 - AVL Trees: companion code for the Thinking Problems (Section 7.18).

Run:  python3 ch07_solutions.py
"""

from __future__ import annotations

import ch07_examples as avl


def fib(k: int) -> int:
    """F(1) = F(2) = 1 (the formal proof of Section 7.9: N(h) + 1 = F(h + 3))."""
    a, b = 0, 1
    for _ in range(k):
        a, b = b, a + b
    return a


def shallowest_leaf(n) -> int:
    """Thinking Problem 1: the depth of the shallowest leaf (-1 for an empty tree)."""
    if n is None:
        return -1
    if n.left is None and n.right is None:
        return 0
    return 1 + min(shallowest_leaf(c) for c in (n.left, n.right) if c is not None)


# Thinking Problem 2: an AVL tree whose nodes also store the size of their subtree, so that the k-th smallest
# key can be found in O(log n). The code is Chapter 7's, with `size` kept beside `height`.

class SNode:
    __slots__ = ("key", "left", "right", "height", "size")

    def __init__(self, key):
        self.key, self.left, self.right, self.height, self.size = key, None, None, 0, 1


def size(n) -> int:
    return 0 if n is None else n.size


def update(n) -> None:
    n.height = 1 + max(avl.h(n.left), avl.h(n.right))
    n.size = 1 + size(n.left) + size(n.right)            # the only new line: O(1) more per node


def rotate_right(y):
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


def rebalance(n):
    update(n)
    if avl.balance(n) > 1:
        if avl.balance(n.left) < 0:
            n.left = rotate_left(n.left)
        return rotate_right(n)
    if avl.balance(n) < -1:
        if avl.balance(n.right) > 0:
            n.right = rotate_right(n.right)
        return rotate_left(n)
    return n


def insert(n, key):
    if n is None:
        return SNode(key)
    if key < n.key:
        n.left = insert(n.left, key)
    elif key > n.key:
        n.right = insert(n.right, key)
    else:
        return n
    return rebalance(n)


def delete(n, key):
    if n is None:
        return None
    if key < n.key:
        n.left = delete(n.left, key)
    elif key > n.key:
        n.right = delete(n.right, key)
    else:
        if n.left is None or n.right is None:
            return n.left or n.right
        s = n.right
        while s.left is not None:
            s = s.left
        n.key = s.key
        n.right = delete(n.right, s.key)
    return rebalance(n)


def select(n, k):
    """The k-th smallest key (k = 1 is the smallest), or None if there is no such key. O(height)."""
    while n is not None:
        r = size(n.left) + 1                              # n's rank inside its own subtree
        if k == r:
            return n.key
        if k < r:
            n = n.left
        else:
            k -= r
            n = n.right
    return None


def sizes_correct(n) -> bool:
    return n is None or (n.size == 1 + size(n.left) + size(n.right) and sizes_correct(n.left)
                         and sizes_correct(n.right))


# Thinking Problem 3: the "stop when the height has not changed" shortcut, wrongly used for deletion.

def delete_early_stop(n, key):
    """Returns (new root, done). Plain BST deletion; on the way up, a node whose height did not change
    stops all further work, without checking its balance factor. Wrong: see Thinking Problem 3."""
    if n is None:
        return None, True
    if key < n.key:
        n.left, done = delete_early_stop(n.left, key)
    elif key > n.key:
        n.right, done = delete_early_stop(n.right, key)
    else:
        if n.left is None or n.right is None:
            return n.left or n.right, False
        s = n.right
        while s.left is not None:
            s = s.left
        n.key = s.key
        n.right, done = delete_early_stop(n.right, s.key)
    if done:
        return n, True
    old = n.height
    avl.update(n)
    if n.height == old:                                   # the shortcut: nothing above can change ...
        return n, True                                    # ... but n itself may now be at -2 or +2
    return avl.rebalance(n), False


if __name__ == "__main__":
    for hh in range(0, 9):
        t = avl.sparsest(hh)
        print(hh, avl.fewest_nodes(hh), shallowest_leaf(t), -(-hh // 2))
    root = None
    for k in [58, 25, 91, 12, 70, 47, 84, 31, 63]:
        root = insert(root, k)
    print([select(root, k) for k in range(0, 11)])
    t, _ = delete_early_stop(avl.build([20, 10, 30, 40]), 10)
    print(avl.shape(t), avl.balance(t), avl.is_avl(t))
