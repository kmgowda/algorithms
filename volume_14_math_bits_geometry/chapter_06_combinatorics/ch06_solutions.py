"""Volume 14, Chapter 6 - Solutions to the exercises."""

from __future__ import annotations

from collections import Counter

from ch06_examples import catalan, combinations_count


def unique_paths(rows: int, cols: int) -> int:
    """Exercise 1 (LeetCode 62): a route is a sequence of (rows-1) downs and (cols-1) rights - choose the downs."""
    return combinations_count(rows + cols - 2, rows - 1)


def num_trees(n: int) -> int:
    """Exercise 2 (LeetCode 96): the number of BST shapes with n keys is the n-th Catalan number."""
    return catalan(n)


def anagram_count(word: str) -> int:
    """Exercise 3: distinct rearrangements of a word with repeated letters: n! / (count_1! count_2! ...)."""
    total, remaining = 1, len(word)
    for c in Counter(word).values():
        total *= combinations_count(remaining, c)
        remaining -= c
    return total


def round_table(n: int) -> int:
    """Exercise 4: seatings of n people around a round table (rotations are the same) = (n - 1)!."""
    out = 1
    for i in range(2, n):
        out *= i
    return out


if __name__ == "__main__":
    print(unique_paths(3, 7), num_trees(3), anagram_count("BANANA"), round_table(10))
