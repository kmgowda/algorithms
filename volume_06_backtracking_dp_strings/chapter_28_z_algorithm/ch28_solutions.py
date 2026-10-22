"""Volume 6, Chapter 28 - Thinking Problems.

Problem 1: building the Z-array of n letters takes at most 2n letter comparisons (checked).
Problem 2: is one word a rotation of another? Search for it in the other written twice: O(n) with the Z-array.
Problem 3: without the separator, a match can run from the pattern into the text and report a false position.
"""

from __future__ import annotations

from ch28_examples import z_array, z_search


def is_rotation(a: str, b: str) -> bool:
    return len(a) == len(b) and (not a or bool(z_search(b + b, a)))


def z_search_no_sep(text: str, pattern: str) -> list:
    z, _ = z_array(pattern + text)
    m = len(pattern)
    return [i - m for i in range(1, len(z)) if z[i] >= m]


if __name__ == "__main__":
    print(is_rotation("library", "rarylib"), is_rotation("library", "yrarbil"))
    print(z_search_no_sep("a", "aa"), z_search("a", "aa"), z_search_no_sep("bab", "ab"), z_search("bab", "ab"))
