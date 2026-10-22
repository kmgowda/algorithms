"""Volume 6, Chapter 3 - model solutions to the Thinking Problems (Section 3.14)."""

from __future__ import annotations


def next_combination(c: list, n: int) -> list | None:
    """The k-combination of positions 0..n-1 that follows c in alphabetical order, or None after the last.
    O(k) steps: bump the rightmost position that still has room, then pack the later ones just after it."""
    k = len(c)
    i = k - 1
    while i >= 0 and c[i] == n - k + i:
        i -= 1                                        # this position is as far right as it can go
    if i < 0:
        return None
    out = list(c)
    out[i] += 1
    for j in range(i + 1, k):
        out[j] = out[j - 1] + 1
    return out


def distinct_permutations_reversed(items: list) -> tuple[list, int]:
    """Thinking Problem 1's variant: skip a repeat while its left twin IS used. Returns (orders, nodes)."""
    items, out, used, nodes = sorted(items), [], [False] * len(items), [0]

    def go(row):
        nodes[0] += 1
        if len(row) == len(items):
            out.append(list(row))
            return
        for i, x in enumerate(items):
            if used[i] or (i > 0 and items[i] == items[i - 1] and used[i - 1]):
                continue
            used[i] = True
            row.append(x)
            go(row)
            row.pop()
            used[i] = False

    go([])
    return out, nodes[0]
