"""Volume 6, Chapter 14 - Thinking Problems.

Problem 1: one row filled from the right equals the full table's last row (checked on random shelves).
Problem 2: the most votes with at most k books as well as the budget: one more dimension, O(n k budget).
Problem 3: a free book with unlimited copies used to give a finite answer (5 votes for £3); it is now refused.
"""

from __future__ import annotations

import itertools


def best_with_limit(books: list, budget: int, k: int) -> int:
    """best[c][b]: most votes with at most c books and b pounds; each book at most once."""
    best = [[0] * (budget + 1) for _ in range(k + 1)]
    for _, price, votes in books:
        for c in range(k, 0, -1):
            for b in range(budget, price - 1, -1):
                best[c][b] = max(best[c][b], best[c - 1][b - price] + votes)
    return best[k][budget]


def brute_limit(books: list, budget: int, k: int) -> int:
    return max((sum(v for *_, v in c) for m in range(min(k, len(books)) + 1)
                for c in itertools.combinations(books, m) if sum(p for _, p, _ in c) <= budget), default=0)


if __name__ == "__main__":
    from ch14_examples import BOOKS, knapsack, knapsack_one_row
    print(knapsack(BOOKS, 20)[0], knapsack_one_row(BOOKS, 20), [best_with_limit(BOOKS, 20, k) for k in range(5)])
