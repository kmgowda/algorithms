"""Volume 4, Chapter 12 - Thinking Problems (Section 12.16): model solutions that can be run.

1. optimal_merge_comparisons: the fewest comparisons that can merge two sorted shelves, by brute force over every
   decision tree (it confirms 2n - 1, not the counting bound, for shelves of n and n).
2. sort_few_distinct: sort n items with only k distinct values in O(n log k) comparisons.
3. rosa_sort5 and ford_johnson5: two ways to sort five items; only the second always stays within 7 comparisons.

Run:  python3 ch12_solutions.py
"""

from __future__ import annotations

import itertools
import math
from functools import lru_cache


# ---------------------------------------------------------------- Thinking Problem 1: merging needs 2n - 1

def optimal_merge_comparisons(m: int, n: int) -> int:
    """Fewest comparisons that guarantee merging sorted shelves of m and n distinct books, over all methods.
    An outcome is an interleaving (which positions hold the first shelf); a comparison 'a_i < b_j?' splits the
    interleavings still possible. Minimax over every comparison: the height of the best decision tree."""
    outcomes = frozenset(itertools.combinations(range(m + n), m))

    def a_before_b(pos_a, i, j):                    # is a_i before b_j in this interleaving?
        p = pos_a[i]
        b_positions = [q for q in range(m + n) if q not in pos_a]
        return p < b_positions[j]

    @lru_cache(maxsize=None)
    def best(still: frozenset) -> int:
        if len(still) <= 1:
            return 0
        result = math.inf
        for i in range(m):
            for j in range(n):
                yes = frozenset(o for o in still if a_before_b(o, i, j))
                if 0 < len(yes) < len(still):
                    result = min(result, 1 + max(best(yes), best(still - yes)))
        return result

    return best(outcomes)


def merge_counting_bound(m: int, n: int) -> int:
    """The counting bound of Challenge 1: ceil(log2 C(m + n, m))."""
    return (math.comb(m + n, m) - 1).bit_length()


# ---------------------------------------------------------------- Thinking Problem 2: few distinct values

def sort_few_distinct(a: list) -> tuple[list, int]:
    """Sort a when it holds few distinct values: keep the distinct values seen so far in a sorted list with a count
    each, and find each item's value by binary search. Returns (sorted list, comparisons made).
    With k distinct values each item costs at most ceil(log2(k + 1)) + 1 comparisons."""
    values, counts, comparisons = [], [], 0
    for x in a:
        lo, hi = 0, len(values)
        while lo < hi:                                  # first value that is not smaller than x
            mid = (lo + hi) // 2
            comparisons += 1
            if values[mid] < x:
                lo = mid + 1
            else:
                hi = mid
        if lo < len(values):
            comparisons += 1
        if lo < len(values) and values[lo] == x:
            counts[lo] += 1
        else:
            values.insert(lo, x)
            counts.insert(lo, 1)
    return [v for v, c in zip(values, counts) for _ in range(c)], comparisons


def few_distinct_bound(n: int, k: int) -> int:
    """The guarantee of the model solution: n * (ceil(log2(k + 1)) + 1) comparisons."""
    return n * ((k).bit_length() + 1) if n else 0


# ---------------------------------------------------------------- Thinking Problem 3: five books in 7?

def _insert(chain: list, x, limit: int, tally: list) -> None:
    """Binary insertion of x among chain[0:limit], counting comparisons in tally[0]."""
    lo, hi = 0, limit
    while lo < hi:
        mid = (lo + hi) // 2
        tally[0] += 1
        if x < chain[mid]:
            hi = mid
        else:
            lo = mid + 1
    chain.insert(lo, x)


def _three_comparisons(x: tuple, tally: list) -> tuple[list, object, object]:
    """Steps 1-3 of both methods: sort the pairs (a, b) and (c, d), then compare their larger books.
    Returns the chain p < q < s, the book r known to be below s, and the fifth book e."""
    a, b, c, d, e = x
    tally[0] += 1
    if b < a:
        a, b = b, a
    tally[0] += 1
    if d < c:
        c, d = d, c
    tally[0] += 1
    if d < b:
        a, b, c, d = c, d, a, b
    return [a, b, d], c, e


def rosa_sort5(x: tuple) -> tuple[list, int]:
    """Rosa's plan: insert the paired book r below s first, then insert e into the chain of four."""
    tally = [0]
    chain, r, e = _three_comparisons(x, tally)
    _insert(chain, r, 2, tally)                          # r < s = chain[2]: search the two books below s
    _insert(chain, e, len(chain), tally)
    return chain, tally[0]


def ford_johnson5(x: tuple) -> tuple[list, int]:
    """The repair (Ford and Johnson): insert e into the chain of three first, then r below s."""
    tally = [0]
    chain, r, e = _three_comparisons(x, tally)
    s = chain[2]
    _insert(chain, e, 3, tally)
    _insert(chain, r, chain.index(s), tally)             # r < s: search only the books below s
    return chain, tally[0]


def worst_over_orders(sort5) -> tuple[int, tuple]:
    """The largest comparison count over all 120 orders of five distinct books, and the first order reaching it."""
    worst, witness = -1, None
    for p in itertools.permutations((12, 25, 31, 47, 58)):
        out, comps = sort5(p)
        assert out == sorted(p)
        if comps > worst:
            worst, witness = comps, p
    return worst, witness


if __name__ == "__main__":
    print([(n, merge_counting_bound(n, n), optimal_merge_comparisons(n, n)) for n in range(1, 6)])
    print(sort_few_distinct([58, 25, 58, 12, 25, 47, 58, 12, 47]))
    print(worst_over_orders(rosa_sort5), worst_over_orders(ford_johnson5), rosa_sort5((31, 47, 12, 58, 25)))
