"""Volume 4, Chapter 6 - Quicksort: model solutions to the Thinking Problems (Section 6.15).

Run:  python3 ch06_solutions.py
"""

from __future__ import annotations

import itertools
import random


def match_jackets(books: list, jackets: list, rng=None, counter: dict | None = None) -> list:
    """Thinking Problem 2: pair every book with the dust jacket of the same size, comparing only a book with a
    jacket (never two books or two jackets). Random jacket as pivot: split the books around it, the matching book
    then splits the jackets. Returns the (book, jacket) pairs from smallest to largest; expected O(n log n)."""
    rng = rng or random.Random(1)

    def fits(book, jacket):                       # the only comparison allowed: -1 too small, 0 fits, +1 too big
        if counter is not None:
            counter["comparisons"] += 1
        return (book > jacket) - (book < jacket)

    def solve(bs, js):
        if not bs:
            return []
        jacket = js[rng.randrange(len(js))]
        small_b, large_b, match = [], [], None
        for b in bs:
            side = fits(b, jacket)
            if side == 0:
                match = b
            (small_b if side < 0 else large_b if side > 0 else []).append(b)
        small_j, large_j = [], []
        for j in js:
            if j is not jacket:
                (small_j if fits(match, j) > 0 else large_j).append(j)
        return solve(small_b, small_j) + [(match, jacket)] + solve(large_b, large_j)

    if sorted(books) != sorted(jackets):
        raise ValueError("every book needs exactly one jacket of its size")
    return solve(list(books), list(jackets))


def lomuto_comparisons(a: list) -> int:
    """Comparisons of the chapter's last-item Lomuto quicksort (a copy is sorted)."""
    a, count, stack = list(a), 0, [(0, len(a) - 1)]
    while stack:
        lo, hi = stack.pop()
        if lo >= hi:
            continue
        pivot, i = a[hi], lo
        for j in range(lo, hi):
            count += 1
            if a[j] < pivot:
                a[i], a[j] = a[j], a[i]
                i += 1
        a[i], a[hi] = a[hi], a[i]
        stack += [(lo, i - 1), (i + 1, hi)]
    return count


def worst_inputs(n: int) -> list:
    """Thinking Problem 1: every order of 1..n on which last-item quicksort makes n(n - 1)/2 comparisons."""
    return [p for p in itertools.permutations(range(1, n + 1)) if lomuto_comparisons(p) == n * (n - 1) // 2]


def buggy_quicksort_calls(a: list, limit: int = 50) -> list:
    """Thinking Problem 3: the slip Quicksort(a, lo, i) instead of (a, lo, i - 1). Returns the (lo, hi) calls made,
    stopping after `limit` calls; on [12, 25] the same call repeats for ever."""
    calls = []

    def qs(lo, hi):
        if len(calls) >= limit:
            return
        calls.append((lo, hi))
        if lo >= hi:
            return
        pivot, i = a[hi], lo
        for j in range(lo, hi):
            if a[j] < pivot:
                a[i], a[j] = a[j], a[i]
                i += 1
        a[i], a[hi] = a[hi], a[i]
        qs(lo, i)                                 # the bug: the pivot's own place is included
        qs(i + 1, hi)

    qs(0, len(a) - 1)
    return calls


if __name__ == "__main__":
    c = {"comparisons": 0}
    print(match_jackets([58, 25, 91, 12, 70, 47, 84, 31, 63], [63, 12, 84, 25, 91, 31, 47, 70, 58], counter=c), c)
    print([len(worst_inputs(n)) for n in range(1, 8)], worst_inputs(3))
    print(buggy_quicksort_calls([12, 25], limit=5))
