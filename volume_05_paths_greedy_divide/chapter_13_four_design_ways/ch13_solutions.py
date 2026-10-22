"""Volume 5, Chapter 13 - model solutions to the Thinking Problems (Section 13.14).

Run:  python3 ch13_solutions.py
"""

from __future__ import annotations

from bisect import bisect_right

import ch13_examples as ex


def half_sets(books: list) -> list:
    """Every set of the given books as (price, votes)."""
    out = [(0, 0)]
    for _, price, votes in books:
        out += [(p + price, v + votes) for p, v in out]
    return out


def meet_in_the_middle(books: list, budget: int) -> int:
    """Thinking Problem 2: the most votes within budget, in O(2^(n/2) * n) time instead of O(2^n * n).
    List every set of each half; sort the right half's sets by price and keep, for each price, the most votes
    of any set at that price or cheaper; then match every left set with the best right set that still fits."""
    mid = len(books) // 2
    left, right = half_sets(books[:mid]), sorted(half_sets(books[mid:]))
    prices, best_up_to, best = [], [], 0
    for p, v in right:
        prices.append(p)
        best_up_to.append(max(v, best_up_to[-1]) if best_up_to else v)
    for p, v in left:
        if p <= budget:
            k = bisect_right(prices, budget - p) - 1   # the dearest right set that still fits
            best = max(best, v + best_up_to[k])
    return best


def ratio_greedy_with_best_single(books: list, budget: int) -> int:
    """Thinking Problem 3's repair: the better of ratio greedy and the single best book that fits.
    Always at least half the best total."""
    g, _ = ex.greedy(books, budget, key=lambda b: -b[2] / b[1])
    single = max((v for _, p, v in books if p <= budget), default=0)
    return max(g, single)


if __name__ == "__main__":
    print(meet_in_the_middle(ex.BOOKS, ex.BUDGET))
    trap = [("Bookmark", 1, 2), ("Encyclopedia", 20, 20)]
    print(ex.greedy(trap, 20, key=lambda b: -b[2] / b[1]), ratio_greedy_with_best_single(trap, 20))
