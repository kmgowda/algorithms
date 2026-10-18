"""Volume 12, Chapter 5 - 2-D DP: Grid Paths, Edit Distance, Longest Common Subsequence.

Run:  python3 ch05_examples.py
"""

from __future__ import annotations


def grid_paths_with_blocks(grid: list[str]) -> int:
    """LeetCode 63: routes from top-left to bottom-right moving right/down, '#' cells blocked.
    paths[r][c] = paths[r-1][c] + paths[r][c-1] (0 on a blocked cell)."""
    rows, cols = len(grid), len(grid[0])
    paths = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "#":
                continue
            if r == 0 and c == 0:
                paths[r][c] = 1
            else:
                paths[r][c] = (paths[r - 1][c] if r else 0) + (paths[r][c - 1] if c else 0)
    return paths[-1][-1]


def edit_distance(a: str, b: str) -> int:
    """LeetCode 72: fewest single-character inserts, deletes and replacements turning a into b.
    d[i][j] = distance between a[:i] and b[:j]:
      equal last letters -> d[i-1][j-1]; else 1 + min(replace d[i-1][j-1], delete d[i-1][j], insert d[i][j-1])."""
    m, n = len(a), len(b)
    d = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        d[i][0] = i                       # delete everything
    for j in range(n + 1):
        d[0][j] = j                       # insert everything
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                d[i][j] = 1 + min(d[i - 1][j - 1], d[i - 1][j], d[i][j - 1])
    return d[m][n]


def lcs_length(a: str, b: str) -> int:
    """LeetCode 1143: longest common subsequence. L[i][j] = L[i-1][j-1] + 1 if the last letters match,
    else max(L[i-1][j], L[i][j-1])."""
    m, n = len(a), len(b)
    L = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            L[i][j] = L[i - 1][j - 1] + 1 if a[i - 1] == b[j - 1] else max(L[i - 1][j], L[i][j - 1])
    return L[m][n]


def lcs_string(a: str, b: str) -> str:
    """The subsequence itself: fill the table, then walk back from the corner."""
    m, n = len(a), len(b)
    L = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            L[i][j] = L[i - 1][j - 1] + 1 if a[i - 1] == b[j - 1] else max(L[i - 1][j], L[i][j - 1])
    out, i, j = [], m, n
    while i and j:
        if a[i - 1] == b[j - 1]:
            out.append(a[i - 1])
            i, j = i - 1, j - 1
        elif L[i - 1][j] >= L[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return "".join(reversed(out))


def suggest(word: str, dictionary: list[str], k: int = 3) -> list[str]:
    """Industry example: a spell checker suggests the dictionary words closest by edit distance."""
    return sorted(dictionary, key=lambda w: (edit_distance(word, w), w))[:k]


def line_diff(old: list[str], new: list[str]) -> list[str]:
    """Industry example: a tiny 'diff' - lines in the LCS stay, others are removed (-) or added (+)."""
    m, n = len(old), len(new)
    L = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            L[i][j] = L[i + 1][j + 1] + 1 if old[i] == new[j] else max(L[i + 1][j], L[i][j + 1])
    out, i, j = [], 0, 0
    while i < m and j < n:
        if old[i] == new[j]:
            out.append("  " + old[i])
            i, j = i + 1, j + 1
        elif L[i + 1][j] >= L[i][j + 1]:
            out.append("- " + old[i])
            i += 1
        else:
            out.append("+ " + new[j])
            j += 1
    out += ["- " + x for x in old[i:]] + ["+ " + x for x in new[j:]]
    return out


if __name__ == "__main__":
    print("warehouse routes:", grid_paths_with_blocks(["....", ".#..", "...#", "...."]))
    print("kitten -> sitting:", edit_distance("kitten", "sitting"), "| horse -> ros:", edit_distance("horse", "ros"))
    print("LCS:", lcs_length("ACCGGTCG", "GTCGTTCG"), lcs_string("ACCGGTCG", "GTCGTTCG"))
    print("did you mean:", suggest("recieve", ["receive", "relieve", "recipe", "deceive", "review"]))
    print("\n".join(line_diff(["buy milk", "call mum", "pay rent", "gym"], ["buy milk", "pay rent", "book train", "gym"])))
