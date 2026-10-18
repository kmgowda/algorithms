"""Volume 13, Chapter 9 - Solutions to the exercises."""

from __future__ import annotations

from ch09_examples import manacher_radii


def palindrome_lengths_at_centres(s: str) -> list[int]:
    """Exercise 1: for every letter, the longest odd palindrome centred on it (radius at the letter positions)."""
    return manacher_radii(s)[1::2]


def is_palindrome_query(s: str, i: int, j: int) -> bool:
    """Exercise 2: after one O(n) pass, is s[i..j] a palindrome? Check the radius at its centre."""
    radius = manacher_radii(s)
    centre = i + j + 1                         # position of the middle of s[i..j] in the padded string
    return radius[centre] >= j - i + 1


def longest_palindromic_prefix(s: str) -> str:
    """Exercise 3: the longest palindrome starting at position 0."""
    radius = manacher_radii(s)
    best = 0
    for c, r in enumerate(radius):
        if c - r == 0:                         # palindrome reaches the left edge
            best = max(best, r)
    return s[:best]


if __name__ == "__main__":
    print(palindrome_lengths_at_centres("abaaba"), is_palindrome_query("abaaba", 1, 4), longest_palindromic_prefix("abacdc"))
