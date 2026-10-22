"""Volume 3, Chapter 4 - Recursive Tree Problems: companion code for the Thinking Problems (Section 4.14).

Run:  python3 ch04_solutions.py
"""

from __future__ import annotations

import math


def max_path_sum(root) -> float:
    """Thinking Problem 2: the largest total of any path (at least one node, any start and end), O(n).
    down(n) is the best walk that starts at n and goes down; a path bends at its highest node."""
    best = -math.inf

    def down(n):
        nonlocal best
        if n is None:
            return 0
        left, right = max(0, down(n.left)), max(0, down(n.right))   # a losing side is left out
        best = max(best, n.value + left + right)                      # the best path that bends at n
        return n.value + max(left, right)
    down(root)
    return best


def lca_shortcut(n, a, b):
    """Thinking Problem 3: the popular shortcut. It returns a node as soon as it equals a or b, so it never
    checks that the other target exists."""
    if n is None or n.value in (a, b):
        return n
    left, right = lca_shortcut(n.left, a, b), lca_shortcut(n.right, a, b)
    if left and right:
        return n
    return left or right


def min_depth_bound(n: int) -> int:
    """Thinking Problem 1: the bound floor(log2(n + 1)) - 1 on the minimum depth of a full binary tree."""
    return (n + 1).bit_length() - 2


if __name__ == "__main__":
    from ch04_examples import Node, library
    print(max_path_sum(library()), max_path_sum(Node(-3, Node(-7), Node(-1))))
