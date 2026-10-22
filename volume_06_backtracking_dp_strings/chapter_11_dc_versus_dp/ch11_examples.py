"""Volume 6, Chapter 11 - Divide and Conquer versus Dynamic Programming: independent or overlapping sub-problems?

Run:  python3 ch11_examples.py
"""

from __future__ import annotations

from collections import Counter


def merge_sort_ranges(lo: int, hi: int, seen: Counter) -> None:
    """Record every range merge sort works on (Figure 11.1): the halves never overlap."""
    seen[(lo, hi)] += 1
    if hi - lo > 1:
        mid = (lo + hi) // 2
        merge_sort_ranges(lo, mid, seen)
        merge_sort_ranges(mid, hi, seen)


def choose(n: int, k: int, seen: Counter) -> int:
    """Ways to choose k of n books, by Pascal's rule C(n, k) = C(n-1, k-1) + C(n-1, k) (Figure 11.2): sub-problems repeat."""
    seen[(n, k)] += 1
    if k == 0 or k == n:
        return 1
    return choose(n - 1, k - 1, seen) + choose(n - 1, k, seen)


def choose_table(n: int, k: int) -> tuple[int, int]:
    """Pascal's triangle row by row, each entry once (Figure 11.3). Returns (answer, entries filled)."""
    row, filled = [1], 1
    for i in range(1, n + 1):
        row = [1] + [row[j - 1] + row[j] for j in range(1, i)] + [1]
        filled += len(row)
    return row[k], filled


def sub_problem_graph(n: int, k: int) -> tuple[list, list]:
    """The different sub-problems of choose(n, k) with an arrow from each to the two it needs (Figure 11.4).
    Returns (edges, a fill order): smaller n first, so every arrow points to an earlier entry."""
    edges, seen, todo = [], {(n, k)}, [(n, k)]
    while todo:
        a, b = todo.pop()
        if b == 0 or b == a:
            continue
        for c in ((a - 1, b - 1), (a - 1, b)):
            edges.append(((a, b), c))
            if c not in seen:
                seen.add(c)
                todo.append(c)
    return sorted(edges), sorted(seen)


def summary(seen: Counter) -> tuple[int, int]:
    """(calls made, different sub-problems)."""
    return sum(seen.values()), len(seen)


if __name__ == "__main__":
    for n in (8, 16, 1024):
        s = Counter()
        merge_sort_ranges(0, n, s)
        print("merge", n, summary(s))
    for n, k in ((6, 3), (10, 5), (20, 10)):
        s = Counter()
        print("choose", n, k, choose(n, k, s), summary(s), choose_table(n, k))
    s = Counter()
    choose(6, 3, s)
    print(sorted(s.items()))
