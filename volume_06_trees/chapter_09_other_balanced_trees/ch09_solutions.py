"""Volume 6, Chapter 9 - Solutions to the exercises."""

from __future__ import annotations

from ch09_examples import SplayTree, Treap, TreapNode, height, merge, split


def treap_heights(n: int, seeds: list[int]) -> list[int]:
    """Exercise 1: different random priorities, different shapes - but all short."""
    out = []
    for seed in seeds:
        t = Treap(seed)
        for k in range(n):
            t.insert(k)
        out.append(height(t.root))
    return out


def splay_depth_of_hot_key(keys: int, hot: int, accesses: int) -> int:
    """Exercise 2: after repeatedly searching one 'hot' key, how deep is it? (0 = the root)"""
    t = SplayTree()
    for k in range(keys):
        t.insert(k)
    for _ in range(accesses):
        t.contains(hot)
    depth, node = 0, t.root
    while node is not None and node.key != hot:
        node = node.left if hot < node.key else node.right
        depth += 1
    return depth


def range_split(t: Treap, low: int, high: int) -> list[int]:
    """Exercise 3: keys in [low, high] by splitting the treap twice, then gluing it back together."""
    left, rest = split(t.root, low)
    middle, right = split(rest, high + 1)
    found: list[int] = []

    def walk(node: TreapNode | None) -> None:
        if node is not None:
            walk(node.left)
            found.append(node.key)
            walk(node.right)

    walk(middle)
    t.root = merge(merge(left, middle), right)
    return found


if __name__ == "__main__":
    print(treap_heights(1000, [1, 2, 3]), splay_depth_of_hot_key(100, 42, 5))
    t = Treap(4)
    for k in range(20):
        t.insert(k)
    print(range_split(t, 5, 9))
