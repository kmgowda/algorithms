"""Volume 5, Chapter 9 - Edit Distance: the fewest single-letter changes that turn one word into another.

Run:  python3 ch09_examples.py
"""

from __future__ import annotations

TITLES = ["ATLAS", "NOVEL", "POEMS", "COMIC", "DIARY", "PLAYS", "MAPS", "LIBRARY"]


def edit_distance(a: str, b: str) -> tuple[int, list, list]:
    """D[i][j] = fewest inserts, deletes, and replacements turning a[:i] into b[:j] (Figure 9.2).
    Returns (distance, list of edits, table)."""
    n, m = len(a), len(b)
    D = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        D[i][0] = i                                    # delete everything
    for j in range(m + 1):
        D[0][j] = j                                    # insert everything
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            same = a[i - 1] == b[j - 1]
            D[i][j] = min(D[i - 1][j - 1] + (0 if same else 1),   # keep or replace
                          D[i - 1][j] + 1,                        # delete a[i-1]
                          D[i][j - 1] + 1)                        # insert b[j-1]
    edits, i, j = [], n, m
    while i or j:
        if i and j and D[i][j] == D[i - 1][j - 1] + (a[i - 1] != b[j - 1]):
            if a[i - 1] != b[j - 1]:
                edits.append(f"replace {a[i - 1]} with {b[j - 1]}")
            i, j = i - 1, j - 1
        elif i and D[i][j] == D[i - 1][j] + 1:
            edits.append(f"delete {a[i - 1]}")
            i -= 1
        else:
            edits.append(f"insert {b[j - 1]}")
            j -= 1
    return D[n][m], edits[::-1], D


def suggest(typed: str, titles: list) -> list:
    """Titles sorted by edit distance from what was typed (Section 9.7)."""
    return sorted((edit_distance(typed, t)[0], t) for t in titles)


if __name__ == "__main__":
    print(edit_distance("LIBRAY", "LIBRARY")[:2])
    d, e, t = edit_distance("PEOMS", "POEMS")
    print(d, e)
    for row in t:
        print(row)
    print(edit_distance("KITTEN", "SITTING")[:2])
    print(suggest("PALYS", TITLES)[:3], suggest("NOBEL", TITLES)[:2])
