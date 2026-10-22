"""Volume 6, Chapter 14 - The Knapsack Problem: the reading club's budget, solved exactly with a table.

Run:  python3 ch14_examples.py
"""

from __future__ import annotations

import itertools

BOOKS = [("Atlas", 9, 6), ("Novel", 6, 4), ("Poems", 5, 6), ("Comic", 5, 2), ("Cookbook", 10, 7)]


def knapsack(books: list, budget: int) -> tuple[int, list, list]:
    """best[i][b] = most votes from the first i books with b pounds (Figure 14.2). Returns (votes, names, table)."""
    n = len(books)
    best = [[0] * (budget + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        _, price, votes = books[i - 1]
        for b in range(budget + 1):
            best[i][b] = best[i - 1][b]                               # leave book i
            if price <= b:
                best[i][b] = max(best[i][b], best[i - 1][b - price] + votes)  # take book i
    chosen, b = [], budget
    for i in range(n, 0, -1):
        if best[i][b] != best[i - 1][b]:
            chosen.append(books[i - 1][0])
            b -= books[i - 1][1]
    return best[n][budget], chosen[::-1], best


def knapsack_one_row(books: list, budget: int) -> int:
    """The same answer with a single row, filled from the right so each book is used at most once."""
    row = [0] * (budget + 1)
    for _, price, votes in books:
        for b in range(budget, price - 1, -1):
            row[b] = max(row[b], row[b - price] + votes)
    return row[budget]


def unlimited(books: list, budget: int) -> int:
    """Copies allowed (several of the same book for different groups): fill from the left instead."""
    row = [0] * (budget + 1)
    for _, price, votes in books:
        for b in range(price, budget + 1):
            row[b] = max(row[b], row[b - price] + votes)
    return row[budget]


def subset_sums(prices: list, budget: int) -> list:
    """Which totals up to budget can be spent exactly with whole books (Section 14.7): the knapsack with
    votes equal to price, kept as true/false. reach[t] is True when some set of books costs exactly t."""
    reach = [True] + [False] * budget
    for p in prices:
        for t in range(budget, p - 1, -1):
            reach[t] = reach[t] or reach[t - p]
    return reach


def brute(books: list, budget: int) -> int:
    return max(sum(v for *_, v in c) for k in range(len(books) + 1) for c in itertools.combinations(books, k)
               if sum(p for _, p, _ in c) <= budget)


if __name__ == "__main__":
    votes, names, table = knapsack(BOOKS, 20)
    print(votes, names, table[-1])
    print(knapsack_one_row(BOOKS, 20), unlimited(BOOKS, 20), brute(BOOKS, 20))
    print([knapsack(BOOKS, b)[0] for b in range(0, 41, 5)])
