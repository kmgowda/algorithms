"""Volume 5, Chapter 20 - The Z-Algorithm: how far does the string match its own beginning, at every position?

Run:  python3 ch20_examples.py
"""

from __future__ import annotations


def z_array(s: str) -> tuple[list, int]:
    """z[i] = length of the longest common prefix of s and s[i:] (Figure 20.2); z[0] = len(s) by convention.
    Reuses the rightmost match box [left, right) found so far. Returns (z, letter comparisons)."""
    n = len(s)
    z = [0] * n
    if n:
        z[0] = n
    left = right = 0
    comparisons = 0
    for i in range(1, n):
        if i < right:
            z[i] = min(right - i, z[i - left])        # copy what the box already tells us
        while i + z[i] < n:
            comparisons += 1
            if s[z[i]] != s[i + z[i]]:
                break
            z[i] += 1
        if i + z[i] > right:
            left, right = i, i + z[i]
    return z, comparisons


def z_search(text: str, pattern: str, sep: str = "\0") -> list:
    """Occurrences of pattern: Z-array of pattern + separator + text; a value of len(pattern) marks a match."""
    if not pattern:
        return list(range(len(text) + 1))
    z, _ = z_array(pattern + sep + text)
    m = len(pattern)
    return [i - m - 1 for i in range(m + 1, len(z)) if z[i] >= m]


if __name__ == "__main__":
    print(z_array("abacaba"), z_array("aabxaab"))
    print(z_search("abacabacab", "abacab"), z_search("the club meets the club", "club"))
    print(z_array("a" * 1000)[1], z_array("ab" * 500)[1])
