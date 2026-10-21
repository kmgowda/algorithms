"""Volume 5, Chapter 29 - Comparing Files: Diff, the LCS of lines shown as kept, deleted, and added lines.

Run:  python3 ch29_examples.py
"""

from __future__ import annotations

import difflib

OLD = ["Welcome to the library", "Opening hours: 9 to 5", "Reading club on Monday", "Ask at the desk", "Thank you"]
NEW = ["Welcome to the library", "Opening hours: 9 to 6", "Reading club on Monday", "Film night on Friday", "Thank you"]


def diff(old: list, new: list) -> list:
    """Lines as ('  ', kept), ('- ', deleted), ('+ ', added), from the LCS table of the two files (Figure 29.2)."""
    n, m = len(old), len(new)
    L = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):                    # filled from the end, so the walk can go forwards
        for j in range(m - 1, -1, -1):
            L[i][j] = L[i + 1][j + 1] + 1 if old[i] == new[j] else max(L[i + 1][j], L[i][j + 1])
    out, i, j = [], 0, 0
    while i < n and j < m:
        if old[i] == new[j]:
            out.append(("  ", old[i])); i += 1; j += 1
        elif L[i + 1][j] >= L[i][j + 1]:
            out.append(("- ", old[i])); i += 1
        else:
            out.append(("+ ", new[j])); j += 1
    out += [("- ", x) for x in old[i:]] + [("+ ", x) for x in new[j:]]
    return out


def apply_diff(old: list, edits: list) -> list:
    """Rebuild the new file from the old one and the diff."""
    return [line for tag, line in edits if tag in ("  ", "+ ")]


def changes(edits: list) -> tuple[int, int, int]:
    return tuple(sum(1 for t, _ in edits if t == tag) for tag in ("  ", "- ", "+ "))


if __name__ == "__main__":
    d = diff(OLD, NEW)
    for tag, line in d:
        print(tag + line)
    print(changes(d), apply_diff(OLD, d) == NEW)
    print([x for x in difflib.ndiff(OLD, NEW) if x[0] in "+- "][:6])
