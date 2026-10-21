"""Volume 4, Chapter 27 - Subsets, Permutations, Combinations: the three basic backtracking shapes.

Run:  python3 ch27_examples.py
"""

from __future__ import annotations

BOOKS = ["Atlas", "Novel", "Poems", "Comic"]


def subsets(items: list) -> list:
    """Every subset: for each item, take it or leave it (Figure 27.2)."""
    out = []

    def go(i, chosen):
        if i == len(items):
            out.append(list(chosen))
            return
        chosen.append(items[i])
        go(i + 1, chosen)
        chosen.pop()
        go(i + 1, chosen)

    go(0, [])
    return out


def permutations(items: list) -> list:
    """Every order: choose any unused item for the next place."""
    out, used = [], [False] * len(items)

    def go(row):
        if len(row) == len(items):
            out.append(list(row))
            return
        for i, x in enumerate(items):
            if not used[i]:
                used[i] = True
                row.append(x)
                go(row)
                row.pop()
                used[i] = False

    go([])
    return out


def combinations(items: list, k: int) -> list:
    """Every choice of k items, in list order: only look at items after the last one chosen."""
    out = []

    def go(start, chosen):
        if len(chosen) == k:
            out.append(list(chosen))
            return
        for i in range(start, len(items)):
            if len(items) - i < k - len(chosen):
                break                                 # not enough items left to finish
            chosen.append(items[i])
            go(i + 1, chosen)
            chosen.pop()

    go(0, [])
    return out


def distinct_permutations(items: list) -> list:
    """Orders of a list with repeats, each different order once: skip a value already tried in this place."""
    items, out, used = sorted(items), [], [False] * len(items)

    def go(row):
        if len(row) == len(items):
            out.append(list(row))
            return
        for i, x in enumerate(items):
            if used[i] or (i > 0 and items[i] == items[i - 1] and not used[i - 1]):
                continue
            used[i] = True
            row.append(x)
            go(row)
            row.pop()
            used[i] = False

    go([])
    return out


if __name__ == "__main__":
    print(len(subsets(BOOKS)), len(permutations(BOOKS)), len(combinations(BOOKS, 2)), combinations(BOOKS, 2))
    print(distinct_permutations(list("AAB")), len(permutations(list("AAB"))))
