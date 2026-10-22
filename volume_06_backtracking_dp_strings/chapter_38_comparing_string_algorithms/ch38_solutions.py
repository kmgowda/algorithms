"""Volume 6, Chapter 38 - model solutions to the Thinking Problems (Section 38.15)."""

from __future__ import annotations


def z_values(s: str) -> list:
    """Z[i] = length of the longest common prefix of s and s[i:] (Z[0] = len(s)), in linear time (Chapter 28)."""
    n = len(s)
    z = [0] * n
    if n:
        z[0] = n
    left = right = 0
    for i in range(1, n):
        if i < right:
            z[i] = min(right - i, z[i - left])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] > right:
            left, right = i, i + z[i]
    return z


def one_mismatch_search(text: str, pattern: str) -> list:
    """Every start where pattern matches text with at most one wrong letter, in O(n + m) (Thinking Problem 2).
    fwd[i]: letters matching forward from i; back[i]: letters matching backward from the window's last letter.
    The window at i fits with at most one mismatch exactly when fwd[i] + back[i] >= m - 1."""
    n, m = len(text), len(pattern)
    if m == 0:
        return list(range(n + 1))
    if m > n:
        return []
    zf = z_values(pattern + "\0" + text)
    zb = z_values(pattern[::-1] + "\0" + text[::-1])
    out = []
    for i in range(n - m + 1):
        fwd = min(zf[m + 1 + i], m)
        back = min(zb[m + 1 + (n - (i + m))], m)
        if fwd + back >= m - 1:
            out.append(i)
    return out


def one_mismatch_brute(text: str, pattern: str) -> list:
    """The slow check: compare every window letter by letter, O(n m)."""
    m = len(pattern)
    return [i for i in range(len(text) - m + 1)
            if sum(a != b for a, b in zip(text[i:i + m], pattern)) <= 1]


def skip_after_match_search(text: str, pattern: str) -> list:
    """Thinking Problem 3's plausible bug: after a match, jump past the whole match, so overlapping matches are lost."""
    m = len(pattern)
    out, i = [], 0
    while m and i + m <= len(text):
        if text[i:i + m] == pattern:
            out.append(i)
            i += m
        else:
            i += 1
    return out
