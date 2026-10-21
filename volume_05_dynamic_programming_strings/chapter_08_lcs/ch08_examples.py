"""Volume 5, Chapter 8 - Longest Common Subsequence: what two sequences share, in the same order.

Run:  python3 ch08_examples.py
"""

from __future__ import annotations

import itertools

ANA = ["Atlas", "Poems", "Maps", "Novel", "Comic", "Diary", "Plays"]
BEN = ["Poems", "Atlas", "Novel", "Diary", "Maps", "Plays"]


def lcs(a, b) -> tuple[int, list, list]:
    """L[i][j] = length of the longest common subsequence of a[:i] and b[:j] (Figure 8.2).
    Returns (length, one longest common subsequence, table)."""
    n, m = len(a), len(b)
    L = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1              # match: extend the diagonal
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])    # drop the last item of one or the other
    out, i, j = [], n, m
    while i and j:
        if a[i - 1] == b[j - 1]:
            out.append(a[i - 1]); i -= 1; j -= 1
        elif L[i - 1][j] >= L[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return L[n][m], out[::-1], L


def brute(a, b) -> int:
    for k in range(min(len(a), len(b)), -1, -1):
        subs = {tuple(c) for c in itertools.combinations(a, k)}
        if any(tuple(c) in subs for c in itertools.combinations(b, k)):
            return k
    return 0


if __name__ == "__main__":
    print(lcs(ANA, BEN)[:2])
    n, s, t = lcs("READING", "TRADING")
    print(n, "".join(s))
    for row in t:
        print(row)
