"""Volume 6, Chapter 1 - model solutions to the Thinking Problems (Section 1.14)."""

from __future__ import annotations

from math import factorial


def kth_seating(readers: list, k: int) -> list:
    """The k-th seating (k = 0, 1, ...) in alphabetical order, without exploring the tree.
    Each first-seat branch holds (n-1)! leaves, so whole subtrees are skipped by counting. O(n^2)."""
    left = sorted(readers)
    if not 0 <= k < factorial(len(left)):
        raise IndexError("k is outside 0 .. n! - 1")
    row = []
    while left:
        block = factorial(len(left) - 1)
        i, k = divmod(k, block)
        row.append(left.pop(i))
    return row


def tree_nodes_floor_e(n: int) -> bool:
    """Thinking Problem 1: the tree for n >= 1 readers has exactly floor(e * n!) nodes (checked exactly)."""
    total = sum(factorial(n) // factorial(k) for k in range(n + 1))
    # e * n! = total + tail, with 0 < tail < 1 for n >= 1; check total < e*n! < total + 1 using e's series to n + 20
    from fractions import Fraction
    e_n = sum(Fraction(factorial(n), factorial(k)) for k in range(n + 21))
    return total < e_n < total + 1


if __name__ == "__main__":
    print(kth_seating(["Ana", "Ben", "Cai", "Dev"], 13), [tree_nodes_floor_e(n) for n in range(1, 11)])
