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


REQUESTS = {12: 9, 25: 5, 47: 1, 63: 2, 84: 3}      # requests a day for five call numbers (Section 11.8)


def optimal_bst(keys: list, freq: list) -> tuple[int, list]:
    """Fewest total looks for searches with known frequencies: cost[i][j] covers keys[i:j].
    Returns (total looks, root) where root[i][j] is the index of the best root of keys[i:j]."""
    n = len(keys)
    cost = [[0] * (n + 1) for _ in range(n + 1)]
    root = [[None] * (n + 1) for _ in range(n + 1)]
    for length in range(1, n + 1):
        for i in range(n - length + 1):
            j = i + length
            weight = sum(freq[i:j])              # every key in the range sinks one level
            for r in range(i, j):
                c = cost[i][r] + cost[r + 1][j] + weight
                if root[i][j] is None or c < cost[i][j]:
                    cost[i][j], root[i][j] = c, r
    return cost[0][n], root


def build_optimal(keys: list, root: list, i: int = 0, j: int | None = None):
    """The tree described by the root table, as Nodes."""
    j = len(keys) if j is None else j
    if i >= j:
        return None
    r = root[i][j]
    return Node(keys[r], build_optimal(keys, root, i, r), build_optimal(keys, root, r + 1, j))


def looks(node, freq_of: dict, depth: int = 1) -> int:
    """Total looks: each key's requests times its depth (the root is depth 1)."""
    if node is None:
        return 0
    return freq_of[node.value] * depth + looks(node.left, freq_of, depth + 1) + looks(node.right, freq_of, depth + 1)


if __name__ == "__main__":
    t = Node(58, Node(25, Node(12), Node(47)), Node(84, None, Node(91)))
    s = save(t)
    print(s, save(load(s)) == s)
    print(preorder(t), inorder(t))
    r = from_pre_in(preorder(t), inorder(t))
    print(save(r))
    b = balanced_from_sorted([12, 25, 31, 47, 58, 63, 70])
    print(save(b), height(b), height(balanced_from_sorted(list(range(1000)))))
    ks, fs = list(REQUESTS), list(REQUESTS.values())
    total, root = optimal_bst(ks, fs)
    opt = build_optimal(ks, root)
    print(total, save(opt), looks(balanced_from_sorted(ks), REQUESTS))
