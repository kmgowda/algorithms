"""Volume 13, Chapter 5 - Solutions to the exercises."""

from __future__ import annotations

from ch05_examples import z_array


def count_distinct_substrings(s: str) -> int:
    """Exercise 1: distinct substrings by adding letters one at a time: the new substrings are suffixes of the
    current prefix that did not occur before, found with Z on the reversed prefix. O(n^2)."""
    total, cur = 0, ""
    for ch in s:
        cur += ch
        z = z_array(cur[::-1])
        longest_old = max(z[1:], default=0)
        total += len(cur) - longest_old
    return total


def string_period(s: str) -> int:
    """Exercise 2: the smallest p such that s is a prefix of (s[:p] repeated) - first i with i + z[i] == n."""
    z = z_array(s)
    n = len(s)
    for i in range(1, n):
        if i + z[i] == n:
            return i
    return n


def bad_character_table(pattern: str) -> dict[str, int]:
    """Exercise 3: Horspool's shift for each letter (letters not listed shift by the full pattern length)."""
    m = len(pattern)
    return {ch: m - 1 - i for i, ch in enumerate(pattern[:-1])}


if __name__ == "__main__":
    print(count_distinct_substrings("abab"), string_period("abcabcab"), bad_character_table("needle"))
