"""Volume 5, Chapter 28 - Matching Patterns with Wildcards: ? is any one letter, * is any run of letters.

Run:  python3 ch28_examples.py
"""

from __future__ import annotations

import fnmatch

TITLES = ["treasure island", "the treasure map", "trees of britain", "a tale of two cities", "tress", "island"]


def wildcard(pattern: str, text: str) -> tuple[bool, list]:
    """M[i][j]: does pattern[:i] match text[:j]? (Figure 28.2). Returns (answer, table)."""
    n, m = len(pattern), len(text)
    M = [[False] * (m + 1) for _ in range(n + 1)]
    M[0][0] = True
    for i in range(1, n + 1):
        if pattern[i - 1] == "*":
            M[i][0] = M[i - 1][0]                     # * can match nothing
    for i in range(1, n + 1):
        p = pattern[i - 1]
        for j in range(1, m + 1):
            if p == "*":
                M[i][j] = M[i - 1][j] or M[i][j - 1]   # * matches nothing, or one more letter
            else:
                M[i][j] = M[i - 1][j - 1] and (p == "?" or p == text[j - 1])
    return M[n][m], M


def plain_recursion(pattern: str, text: str, calls: list) -> bool:
    """The same rules without a table: tries every way a * could stretch."""
    calls[0] += 1
    if not pattern:
        return not text
    if pattern[0] == "*":
        return plain_recursion(pattern[1:], text, calls) or (bool(text) and plain_recursion(pattern, text[1:], calls))
    return bool(text) and pattern[0] in ("?", text[0]) and plain_recursion(pattern[1:], text[1:], calls)


def search(pattern: str, titles: list) -> list:
    return [t for t in titles if wildcard(pattern, t)[0]]


if __name__ == "__main__":
    print(search("tre?s*", TITLES), search("*island", TITLES), search("*of*", TITLES), search("t?e *", TITLES))
    print(wildcard("t*s", "tress")[0], wildcard("t*s", "trees")[0], wildcard("t*s", "tree")[0])
    c = [0]
    print(plain_recursion("*a*a*a*b", "a" * 20, c), c[0], wildcard("*a*a*a*b", "a" * 20)[0], 9 * 21)
