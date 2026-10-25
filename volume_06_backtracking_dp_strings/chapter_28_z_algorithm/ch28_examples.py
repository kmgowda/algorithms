"""Volume 6, Chapter 28 - The Z-Algorithm: how far does the string match its own beginning, at every position?

Run:  python3 ch28_examples.py
"""

from __future__ import annotations


def z_array(s: str) -> tuple[list, int]:
    """z[i] = length of the longest common prefix of s and s[i:] (Figure 28.1); z[0] = len(s) by convention.
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


def z_trace(s: str) -> list:
    """The match box step by step (Section 28.4): for each i, (i, box before as (left, right), how z[i] started:
    "outside", "copied" or "copied to the edge", letters compared, z[i])."""
    n = len(s)
    z, left, right, out = [0] * n, 0, 0, []
    if n:
        z[0] = n
    for i in range(1, n):
        box = (left, right)
        if i < right:
            z[i] = min(right - i, z[i - left])
            how = "copied to the edge" if z[i] == right - i else "copied"
        else:
            how = "outside"
        compared = 0
        if how != "copied":                            # a copy strictly inside the box is already final
            while i + z[i] < n:
                compared += 1
                if s[z[i]] != s[i + z[i]]:
                    break
                z[i] += 1
        if i + z[i] > right:
            left, right = i, i + z[i]
        out.append((i, box, how, compared, z[i]))
    return out


def borders_from_z(z: list) -> list:
    """Chapter 26's border table from the Z-array, in linear time (Challenge 2): a match of length z[i] starting at
    i ends at i + z[i] - 1 with a border of length z[i]; shorter borders follow by stepping back one letter."""
    n = len(z)
    fail = [0] * n
    for i in range(1, n):
        if z[i]:
            end = i + z[i] - 1
            fail[end] = max(fail[end], z[i])
    for j in range(n - 2, -1, -1):
        fail[j] = max(fail[j], fail[j + 1] - 1)
    return fail


if __name__ == "__main__":
    print(z_array("abacaba"), z_array("aabxaab"))
    print(z_search("abacabacab", "abacab"), z_search("the club meets the club", "club"))
    print(z_array("a" * 1000)[1], z_array("ab" * 500)[1])
