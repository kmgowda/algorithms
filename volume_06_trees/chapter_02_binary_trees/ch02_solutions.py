"""Volume 6, Chapter 2 - Solutions to the exercises."""

from __future__ import annotations

from ch02_examples import Node


def mirror(node: Node | None) -> Node | None:
    """Exercise 1 (LeetCode 226): swap left and right everywhere."""
    if node is None:
        return None
    node.left, node.right = mirror(node.right), mirror(node.left)
    return node


def same_tree(a: Node | None, b: Node | None) -> bool:
    """Exercise 2 (LeetCode 100): same shape and same values."""
    if a is None or b is None:
        return a is b
    return a.value == b.value and same_tree(a.left, b.left) and same_tree(a.right, b.right)


def max_nodes(height: int) -> int:
    """Exercise 3: a binary tree of height h holds at most 2^(h+1) - 1 nodes."""
    return 2 ** (height + 1) - 1


def min_height(n: int) -> int:
    """Exercise 4: the smallest possible height for n nodes is floor(log2 n)."""
    return n.bit_length() - 1


def sum_values(node: Node | None) -> int:
    """Exercise 5: total of all values (e.g. prize money in a tournament bracket)."""
    return 0 if node is None else node.value + sum_values(node.left) + sum_values(node.right)


if __name__ == "__main__":
    from ch02_examples import from_level_list
    t = from_level_list([1, 2, 3])
    print(same_tree(t, from_level_list([1, 2, 3])), max_nodes(3), min_height(10), sum_values(t))
    m = mirror(t)
    print(m.left.value, m.right.value)  # type: ignore[union-attr]
