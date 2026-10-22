"""Volume 6, Chapter 23 - Thinking Problems.

Problem 1: LCS(a, b) = max over j of forward[j] + backward[j], the identity Hirschberg's split relies on (checked).
Problem 2: edit distance in two rows of length min(n, m) + 1.
Problem 3: "two rows" that are secretly one list (cur = prev) mix the rows and give wrong lengths.
"""

from __future__ import annotations

from ch23_examples import crossing, lcs_full


def edit_distance_small(a: str, b: str) -> int:
    if len(b) > len(a):
        a, b = b, a                                    # keep the shorter word along the row
    prev = list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        cur = [i] + [0] * len(b)
        for j in range(1, len(b) + 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] != b[j - 1]))
        prev = cur
    return prev[-1]


def edit_distance_full(a: str, b: str) -> int:
    d = [[i + j if i * j == 0 else 0 for j in range(len(b) + 1)] for i in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (a[i - 1] != b[j - 1]))
    return d[-1][-1]


def lcs_aliased(a: str, b: str) -> int:
    prev = [0] * (len(b) + 1)
    for i in range(1, len(a) + 1):
        cur = prev                                     # the bug: the same list, not a new row
        for j in range(1, len(b) + 1):
            cur[j] = prev[j - 1] + 1 if a[i - 1] == b[j - 1] else max(prev[j], cur[j - 1])
        prev = cur
    return prev[-1]


if __name__ == "__main__":
    k, f, g, s = crossing("READING", "TRADING")
    print(max(s), lcs_full("READING", "TRADING")[0], edit_distance_small("READING", "TRADING"), lcs_aliased("READING", "TRADING"), lcs_aliased("AAA", "A"))
