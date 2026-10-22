"""Volume 6, Chapter 24 - Thinking Problems.

Problem 1: with every length priced, plain recursion on n metres makes exactly 2^n calls (checked).
Problem 2: cutting with a charge of c pounds per cut: best[m] = max(price[m], max over k of price[k] + best[m - k] - c).
Problem 3: the memo and plain versions used to crash on a length no pieces could make; they now report -infinity.
"""

from __future__ import annotations

import itertools


def best_with_cut_cost(n: int, price: dict, c: float) -> float:
    best = [0.0] + [float("-inf")] * n
    for m in range(1, n + 1):
        whole = price.get(m, float("-inf"))
        cut = max((price[k] + best[m - k] - c for k in range(1, m) if k in price and best[m - k] > float("-inf")),
                  default=float("-inf"))
        best[m] = max(whole, cut)
    return best[n]


def brute_cut_cost(n: int, price: dict, c: float) -> float:
    best = float("-inf")
    for mask in range(1 << max(n - 1, 0)):
        cuts = [i + 1 for i in range(n - 1) if mask >> i & 1]
        pieces = [b - a for a, b in zip([0] + cuts, cuts + [n])]
        if all(p in price for p in pieces):
            best = max(best, sum(price[p] for p in pieces) - c * len(cuts))
    return best


if __name__ == "__main__":
    from ch24_examples import PRICE, best_memo, best_plain
    calls = [0]; best_plain(8, PRICE, calls); print(calls[0])
    print([best_with_cut_cost(8, PRICE, c) for c in (0, 1, 3)], best_memo(3, {2: 5}, {}))
