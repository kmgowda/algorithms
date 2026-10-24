"""Volume 6, Chapter 37 - Comparing Files: Diff, the LCS of lines shown as kept, deleted, and added lines.

Run:  python3 ch37_examples.py
"""

from __future__ import annotations

import difflib

OLD = ["Welcome to the library", "Opening hours: 9 to 5", "Reading club on Monday", "Ask at the desk", "Thank you"]
NEW = ["Welcome to the library", "Opening hours: 9 to 6", "Reading club on Monday", "Film night on Friday", "Thank you"]


def diff(old: list, new: list) -> list:
    """Lines as ('  ', kept), ('- ', deleted), ('+ ', added), from the LCS table of the two files (Figure 37.1)."""
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


def myers(old: list, new: list) -> tuple[int, list, list]:
    """Myers' O(ND) diff (Section 37.6). Walk the edit graph: a step right deletes a line of old, a step down adds a
    line of new, and a diagonal ("snake") keeps an equal line for free. For d = 0, 1, 2, ... keep, on each diagonal
    k = x - y, the furthest x reachable with exactly d edits. Returns (D, the diff as (tag, line) pairs like diff(),
    the furthest points reached for each d as {k: (x, y)})."""
    n, m = len(old), len(new)
    best = {1: 0}                                      # best[k] = furthest x on diagonal k
    rounds, history = [], []
    for d in range(n + m + 1):
        frontier = {}
        for k in range(-d, d + 1, 2):
            if k == -d or (k != d and best[k - 1] < best[k + 1]):
                x = best[k + 1]                        # step down from diagonal k + 1: add a line
            else:
                x = best[k - 1] + 1                    # step right from diagonal k - 1: delete a line
            y = x - k
            while x < n and y < m and old[x] == new[y]:
                x, y = x + 1, y + 1                    # follow the snake of equal lines
            best[k] = x
            frontier[k] = (x, y)
            if x >= n and y >= m:
                history.append(dict(best))
                rounds.append(frontier)
                return d, _myers_script(old, new, history), rounds
        history.append(dict(best))
        rounds.append(frontier)
    return 0, [], rounds


def _myers_script(old: list, new: list, history: list) -> list:
    """Walk back through the saved rounds to list kept, deleted, and added lines."""
    x, y = len(old), len(new)
    out = []
    for d in range(len(history) - 1, 0, -1):
        prev = history[d - 1]
        k = x - y
        if k == -d or (k != d and prev.get(k - 1, -1) < prev.get(k + 1, -1)):
            pk = k + 1                                 # came down from diagonal k + 1
        else:
            pk = k - 1                                 # came right from diagonal k - 1
        px = prev[pk]
        py = px - pk
        while x > px + (0 if pk == k + 1 else 1) and y > py + (1 if pk == k + 1 else 0):
            x, y = x - 1, y - 1
            out.append(("  ", old[x]))
        if pk == k + 1:
            y -= 1
            out.append(("+ ", new[y]))
        else:
            x -= 1
            out.append(("- ", old[x]))
    while x > 0 and y > 0:
        x, y = x - 1, y - 1
        out.append(("  ", old[x]))
    return out[::-1]


if __name__ == "__main__":
    d = diff(OLD, NEW)
    for tag, line in d:
        print(tag + line)
    print(changes(d), apply_diff(OLD, d) == NEW)
    print([x for x in difflib.ndiff(OLD, NEW) if x[0] in "+- "][:6])
