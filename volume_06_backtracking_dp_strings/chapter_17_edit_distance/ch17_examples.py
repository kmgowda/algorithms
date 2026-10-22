"""Volume 6, Chapter 17 - Edit Distance: the fewest single-letter changes that turn one word into another.

Run:  python3 ch17_examples.py
"""

from __future__ import annotations

TITLES = ["ATLAS", "NOVEL", "POEMS", "COMIC", "DIARY", "PLAYS", "MAPS", "LIBRARY"]


def edit_distance(a: str, b: str) -> tuple[int, list, list]:
    """D[i][j] = fewest inserts, deletes, and replacements turning a[:i] into b[:j] (Figure 17.2).
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


def edit_distance_value(a: str, b: str) -> int:
    """Only the number: the fewest edits turning a into b (Section 17.4)."""
    n, m = len(a), len(b)
    D = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        D[i][0] = i
    for j in range(m + 1):
        D[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            pair = D[i - 1][j - 1] + (0 if a[i - 1] == b[j - 1] else 1)
            D[i][j] = min(pair, D[i - 1][j] + 1, D[i][j - 1] + 1)
    return D[n][m]


def suggest(typed: str, titles: list) -> list:
    """Titles sorted by edit distance from what was typed (Section 17.5)."""
    return sorted((edit_distance(typed, t)[0], t) for t in titles)


def align(a: str, b: str, match: int = 1, mismatch: int = -1, gap: int = -1) -> tuple[int, str, str, list]:
    """Needleman-Wunsch global alignment (Section 17.6): S[i][j] = best score lining up a[:i] with b[:j], where
    a pair of equal letters scores match, unequal letters mismatch, and a letter against a gap scores gap.
    Returns (score, a with gaps, b with gaps, table). Ties prefer pairing, then a gap in b, then a gap in a."""
    n, m = len(a), len(b)
    S = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        S[i][0] = i * gap
    for j in range(1, m + 1):
        S[0][j] = j * gap
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            pair = S[i - 1][j - 1] + (match if a[i - 1] == b[j - 1] else mismatch)
            S[i][j] = max(pair, S[i - 1][j] + gap, S[i][j - 1] + gap)
    top, bottom, i, j = [], [], n, m
    while i or j:
        if i and j and S[i][j] == S[i - 1][j - 1] + (match if a[i - 1] == b[j - 1] else mismatch):
            top.append(a[i - 1]); bottom.append(b[j - 1]); i -= 1; j -= 1
        elif i and S[i][j] == S[i - 1][j] + gap:
            top.append(a[i - 1]); bottom.append("-"); i -= 1
        else:
            top.append("-"); bottom.append(b[j - 1]); j -= 1
    return S[n][m], "".join(top[::-1]), "".join(bottom[::-1]), S


def alignment_score(top: str, bottom: str, match: int = 1, mismatch: int = -1, gap: int = -1) -> int:
    """Score an alignment written as two equal-length rows with '-' for gaps."""
    return sum(gap if x == "-" or y == "-" else (match if x == y else mismatch) for x, y in zip(top, bottom))


if __name__ == "__main__":
    print(edit_distance("LIBRAY", "LIBRARY")[:2])
    d, e, t = edit_distance("PEOMS", "POEMS")
    print(d, e)
    for row in t:
        print(row)
    print(edit_distance("KITTEN", "SITTING")[:2])
    print(suggest("PALYS", TITLES)[:3], suggest("NOBEL", TITLES)[:2])
