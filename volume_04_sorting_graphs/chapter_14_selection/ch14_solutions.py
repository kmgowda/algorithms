"""Volume 4, Chapter 14 - Thinking Problems: model solutions.

Thinking Problem 1: an input on which the median-of-medians pivot is as lopsided as the guarantee allows.
Thinking Problem 2: the weighted median in expected linear time.
Thinking Problem 3: a plausible two-way selection that never finishes.

Run:  python3 ch14_solutions.py
"""

from __future__ import annotations

import random

import ch14_examples as ex


def mom_bad_input(m: int) -> list[int]:
    """n = 5m items (m odd) on which the median-of-medians pivot has only 3(m + 1)/2 - 1 smaller items
    (Thinking Problem 14.1). Low groups: three small items and two huge ones; the pivot's group: two small items,
    the pivot, two huge; high groups: five huge items."""
    if m < 1 or m % 2 == 0:
        raise ValueError("m must be odd and positive")
    h, pivot = (m + 1) // 2, 10 ** 6
    small, big = iter(range(1, pivot)), iter(range(pivot + 1, 3 * pivot))
    out = []
    for g in range(m):
        if g < h - 1:
            out += [next(small) for _ in range(3)] + [next(big) for _ in range(2)]
        elif g == h - 1:
            out += [next(small), next(small), pivot, next(big), next(big)]
        else:
            out += [next(big) for _ in range(5)]
    return out


def weighted_median(items: list, weights: list, rng=None) -> object:
    """The item x with less than half the total weight on items below x and at most half on items above x
    (Thinking Problem 14.2). Quickselect on weights: expected O(n) with a random pivot."""
    if not items or len(items) != len(weights) or min(weights) <= 0:
        raise ValueError("need items with positive weights")
    rng = rng or random.Random(0)
    pairs, total, below = list(zip(items, weights)), sum(weights), 0
    while True:
        x = rng.choice(pairs)[0]
        smaller = [(v, w) for v, w in pairs if v < x]
        larger = [(v, w) for v, w in pairs if v > x]
        w_small = sum(w for _, w in smaller)
        w_equal = sum(w for v, w in pairs if v == x)
        if 2 * (below + w_small) >= total:              # half or more lies below x: go left
            pairs = smaller
        elif 2 * (total - below - w_small - w_equal) > total:   # more than half lies above x: go right
            below += w_small + w_equal
            pairs = larger
        else:
            return x


def weighted_median_by_sorting(items: list, weights: list) -> object:
    """The same answer the slow way: the first item, in sorted order, whose running weight reaches half."""
    total, run = sum(weights), 0
    for v, w in sorted(zip(items, weights)):
        run += w
        if 2 * run >= total:
            return v
    raise ValueError("need items with positive weights")


def first_pivot_select_buggy(a: list, k: int, max_rounds: int = 100):
    """The plausible but wrong method of Thinking Problem 14.3: pivot = first item, split into < pivot and
    >= pivot, keep one side. Returns (answer or None, sizes of the range in each round)."""
    sizes = []
    for _ in range(max_rounds):
        sizes.append(len(a))
        if len(a) == 1:
            return a[0], sizes
        pivot = a[0]
        left = [x for x in a if x < pivot]
        right = [x for x in a if x >= pivot]
        if k <= len(left):
            a = left
        else:
            a, k = right, k - len(left)
    return None, sizes


if __name__ == "__main__":
    bad = mom_bad_input(5)
    _, p = ex.mom_pivot(bad)
    print(p, sum(x < p for x in bad), sum(x > p for x in bad))
    pile_w = dict(zip([12, 25, 31, 47, 58, 63, 70, 84, 91], [3, 1, 4, 1, 5, 9, 2, 6, 5]))
    print(weighted_median(ex.PILE, [pile_w[x] for x in ex.PILE]))
    print(first_pivot_select_buggy(ex.PILE, 5, 6))
