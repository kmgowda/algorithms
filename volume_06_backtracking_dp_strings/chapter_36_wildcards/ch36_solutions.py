"""Volume 6, Chapter 36 - Thinking Problems.

Problem 1: several stars in a row match exactly what one star matches (checked on random patterns).
Problem 2: the same table in two rows, O(len(text)) memory.
Problem 3: using M[i - 1][j - 1] for a star lets it swallow at most one letter: tr* no longer matches treasure.
"""

from __future__ import annotations

import re


def squash_stars(pattern: str) -> str:
    return re.sub(r"\*+", "*", pattern)


def wildcard_two_rows(pattern: str, text: str) -> bool:
    prev = [True] + [False] * len(text)
    for p in pattern:
        cur = [prev[0] and p == "*"] + [False] * len(text)
        for j in range(1, len(text) + 1):
            if p == "*":
                cur[j] = prev[j] or cur[j - 1]
            else:
                cur[j] = prev[j - 1] and (p == "?" or p == text[j - 1])
        prev = cur
    return prev[-1]


def wildcard_one_letter_star(pattern: str, text: str) -> bool:
    n, m = len(pattern), len(text)
    M = [[False] * (m + 1) for _ in range(n + 1)]
    M[0][0] = True
    for i in range(1, n + 1):
        if pattern[i - 1] == "*":
            M[i][0] = M[i - 1][0]
    for i in range(1, n + 1):
        p = pattern[i - 1]
        for j in range(1, m + 1):
            if p == "*":
                M[i][j] = M[i - 1][j] or M[i - 1][j - 1]      # the bug: one letter at most
            else:
                M[i][j] = M[i - 1][j - 1] and (p == "?" or p == text[j - 1])
    return M[n][m]


if __name__ == "__main__":
    from ch36_examples import wildcard
    print(wildcard_two_rows("tre?sure*", "treasure island"), wildcard_one_letter_star("tr*", "treasure"), wildcard("tr*", "treasure")[0], wildcard_one_letter_star("tr*", "tre"))
