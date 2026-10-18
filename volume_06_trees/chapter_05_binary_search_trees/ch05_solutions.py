"""Volume 6, Chapter 5 - Solutions to the exercises."""

from __future__ import annotations

from typing import Any

from ch05_examples import BST, Node


def kth_smallest(tree: BST, k: int) -> Any:
    """Exercise 1 (LeetCode 230): the k-th key of the inorder walk (k from 1)."""
    for i, key in enumerate(tree.keys(), 1):
        if i == k:
            return key
    raise IndexError("k too large")


def lca_bst(node: Node | None, a: Any, b: Any) -> Any:
    """Exercise 2 (LeetCode 235): in a BST, walk down until a and b fall on different sides."""
    while node is not None:
        if a < node.key and b < node.key:
            node = node.left
        elif a > node.key and b > node.key:
            node = node.right
        else:
            return node.key
    return None


def from_sorted(keys: list[Any]) -> BST:
    """Exercise 3 (LeetCode 108): build a BALANCED BST from sorted keys - the middle key becomes the root."""
    tree = BST()

    def build(lo: int, hi: int) -> None:
        if lo > hi:
            return
        mid = (lo + hi) // 2
        tree.insert(keys[mid])
        build(lo, mid - 1)
        build(mid + 1, hi)

    build(0, len(keys) - 1)
    return tree


def closest_key(tree: BST, target: float) -> Any:
    """Exercise 4 (LeetCode 270): the key nearest to target - compare floor and ceiling."""
    low, high = tree.floor(target), tree.ceiling(target)
    candidates = [k for k in (low, high) if k is not None]
    return min(candidates, key=lambda k: (abs(k - target), k))


if __name__ == "__main__":
    t = from_sorted(list(range(1, 16)))
    print(t.height(), kth_smallest(t, 4), lca_bst(t.root, 3, 6), closest_key(t, 7.6))
