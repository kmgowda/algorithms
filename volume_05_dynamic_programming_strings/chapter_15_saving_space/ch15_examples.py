"""Volume 5, Chapter 15 - Saving Space and Rebuilding Answers: keep only the rows you need, and pay for it when rebuilding.

Run:  python3 ch15_examples.py
"""

from __future__ import annotations

import random


def lcs_full(a: str, b: str) -> tuple[int, str, int]:
    """Full table: length, one LCS, and the number of cells stored."""
    n, m = len(a), len(b)
    L = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            L[i][j] = L[i - 1][j - 1] + 1 if a[i - 1] == b[j - 1] else max(L[i - 1][j], L[i][j - 1])
    out, i, j = [], n, m
    while i and j:
        if a[i - 1] == b[j - 1]:
            out.append(a[i - 1]); i -= 1; j -= 1
        elif L[i - 1][j] >= L[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return L[n][m], "".join(reversed(out)), (n + 1) * (m + 1)


def lcs_two_rows(a: str, b: str) -> tuple[int, int]:
    """Length only, keeping two rows (Figure 15.2). Returns (length, cells stored)."""
    prev = [0] * (len(b) + 1)
    for i in range(1, len(a) + 1):
        cur = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            cur[j] = prev[j - 1] + 1 if a[i - 1] == b[j - 1] else max(prev[j], cur[j - 1])
        prev = cur
    return prev[-1], 2 * (len(b) + 1)


def last_row(a: str, b: str) -> list:
    prev = [0] * (len(b) + 1)
    for ch in a:
        cur = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            cur[j] = prev[j - 1] + 1 if ch == b[j - 1] else max(prev[j], cur[j - 1])
        prev = cur
    return prev


def hirschberg(a: str, b: str) -> str:
    """An LCS in little memory (Figure 15.3): split a in half, find where the best path crosses the middle using two
    length-only passes (forwards and backwards), and solve the two halves separately."""
    if not a or not b:
        return ""
    if len(a) == 1:
        return a if a in b else ""
    mid = len(a) // 2
    left = last_row(a[:mid], b)
    right = last_row(a[mid:][::-1], b[::-1])[::-1]
    k = max(range(len(b) + 1), key=lambda j: left[j] + right[j])
    return hirschberg(a[:mid], b[:k]) + hirschberg(a[mid:], b[k:])


if __name__ == "__main__":
    print(lcs_full("READING", "TRADING"), lcs_two_rows("READING", "TRADING"), hirschberg("READING", "TRADING"))
    r = random.Random(15)
    a = "".join(r.choice("ACGT") for _ in range(2000))
    b = "".join(r.choice("ACGT") for _ in range(2000))
    n1, s1, c1 = lcs_full(a, b)
    n2, c2 = lcs_two_rows(a, b)
    s3 = hirschberg(a, b)
    print(n1, n2, len(s3), c1, c2)
