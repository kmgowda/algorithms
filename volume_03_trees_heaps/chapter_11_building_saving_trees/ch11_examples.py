"""Volume 3, Chapter 11 - Building and Saving Trees.

Run:  python3 ch11_examples.py
"""

from __future__ import annotations


class Node:
    def __init__(self, value, left=None, right=None):
        self.value, self.left, self.right = value, left, right


def save(n) -> str:
    """Preorder with '#' for every empty spot (Figure 11.1)."""
    out = []

    def walk(x):
        if x is None:
            out.append("#")
            return
        out.append(str(x.value))
        walk(x.left)
        walk(x.right)
    walk(n)
    return " ".join(out)


def load(text: str):
    """Read the preorder tokens back: each value is followed by its left and right subtrees (Figure 11.2)."""
    tokens = iter(text.split())

    def build():
        t = next(tokens)
        if t == "#":
            return None
        node = Node(int(t))
        node.left = build()
        node.right = build()
        return node
    return build()


def complete(text: str) -> bool:
    """Is this a whole saved tree (Practice Problem 11.3)? Start owing one subtree; a value fills one spot
    and opens two, a # fills one. The line is whole when the debt reaches 0 exactly at its last token."""
    owed = 1
    for t in text.split():
        if owed == 0:
            return False                               # tokens left over after the tree closed
        owed += 1 if t != "#" else -1
    return owed == 0


def from_pre_in(pre: list, ino: list):
    """Rebuild from preorder and inorder (distinct values): the first preorder value is the root (Figure 11.3)."""
    where = {v: i for i, v in enumerate(ino)}
    nxt = iter(pre)

    def build(lo, hi):
        if lo > hi:
            return None
        v = next(nxt)
        node = Node(v)
        node.left = build(lo, where[v] - 1)
        node.right = build(where[v] + 1, hi)
        return node
    return build(0, len(ino) - 1)


def balanced_from_sorted(keys: list, lo: int = 0, hi: int | None = None):
    """Section 11.7: the middle key becomes the root; each half builds a subtree. O(n)."""
    hi = len(keys) - 1 if hi is None else hi
    if lo > hi:
        return None
    mid = (lo + hi) // 2
    return Node(keys[mid], balanced_from_sorted(keys, lo, mid - 1), balanced_from_sorted(keys, mid + 1, hi))


def preorder(n):
    return [] if n is None else [n.value] + preorder(n.left) + preorder(n.right)


def inorder(n):
    return [] if n is None else inorder(n.left) + [n.value] + inorder(n.right)


def height(n):
    return -1 if n is None else 1 + max(height(n.left), height(n.right))


if __name__ == "__main__":
    t = Node(58, Node(25, Node(12), Node(47)), Node(84, None, Node(91)))
    s = save(t)
    print(s, save(load(s)) == s)
    print(preorder(t), inorder(t))
    r = from_pre_in(preorder(t), inorder(t))
    print(save(r))
    b = balanced_from_sorted([12, 25, 31, 47, 58, 63, 70])
    print(save(b), height(b), height(balanced_from_sorted(list(range(1000)))))
