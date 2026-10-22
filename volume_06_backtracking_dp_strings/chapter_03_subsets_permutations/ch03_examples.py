"""Volume 6, Chapter 3 - Subsets, Permutations, Combinations: the three basic backtracking shapes.

Run:  python3 ch03_examples.py
"""

from __future__ import annotations

BOOKS = ["Atlas", "Novel", "Poems", "Comic"]


def subsets(items: list) -> list:
    """Every subset: for each item, take it or leave it (Figure 3.2)."""
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


def output_cost(n: int) -> dict:
    """Section 3.6: items written out when listing every subset and every order of n items.
    Subsets write n * 2^(n-1) items in all (each item is in half of them); orders write n * n!."""
    items = list(range(n))
    return {"subsets": len(subsets(items)), "subset items": sum(map(len, subsets(items))),
            "orders": len(permutations(items)), "order items": sum(map(len, permutations(items)))}


# One book from each genre for the reading week: each position has its own list of options.
GENRES = [("poetry", ["Odes", "Haiku"]), ("maps", ["Atlas"]), ("science", ["Stars", "Cells", "Rocks"])]


def cartesian(options: list) -> list:
    """Every way to pick one option for each position (Figure 3.4): positions are fixed, choices differ."""
    out = []

    def go(i, chosen):
        if i == len(options):
            out.append(list(chosen))
            return
        for x in options[i]:
            chosen.append(x)
            go(i + 1, chosen)
            chosen.pop()

    go(0, [])
    return out


def brackets(n: int, valid_only: bool = True) -> tuple[list, int]:
    """Every balanced string of n pairs of brackets (Figure 3.5). valid_only=True only ever adds a bracket that keeps
    the string fixable: '(' while fewer than n are open, ')' while it closes an open one.
    valid_only=False builds all 2^(2n) strings and checks each at the end. Returns (strings, nodes)."""
    out, nodes = [], [0]

    def balanced(s):
        depth = 0
        for ch in s:
            depth += 1 if ch == "(" else -1
            if depth < 0:
                return False
        return depth == 0

    def go(s, opened, closed):
        nodes[0] += 1
        if len(s) == 2 * n:
            if valid_only or balanced(s):
                out.append(s)
            return
        if not valid_only or opened < n:
            go(s + "(", opened + 1, closed)
        if not valid_only or closed < opened:
            go(s + ")", opened, closed + 1)

    go("", 0, 0)
    return out, nodes[0]


def catalan(n: int) -> int:
    """The number of balanced strings of n pairs: C(2n, n) / (n + 1)."""
    c = 1
    for k in range(n):
        c = c * 2 * (2 * k + 1) // (k + 2)
    return c


def next_permutation(row: list) -> list | None:
    """The order that comes next alphabetically, or None after the last (Challenge 3.2)."""
    a = list(row)
    i = len(a) - 2
    while i >= 0 and a[i] >= a[i + 1]:
        i -= 1                                        # the rightmost place that can still be increased
    if i < 0:
        return None
    j = len(a) - 1
    while a[j] <= a[i]:
        j -= 1                                        # the smallest larger value to its right
    a[i], a[j] = a[j], a[i]
    a[i + 1:] = reversed(a[i + 1:])                   # the tail was falling; reversing sorts it
    return a


if __name__ == "__main__":
    print(len(subsets(BOOKS)), len(permutations(BOOKS)), len(combinations(BOOKS, 2)), combinations(BOOKS, 2))
    print(distinct_permutations(list("AAB")), len(permutations(list("AAB"))))
