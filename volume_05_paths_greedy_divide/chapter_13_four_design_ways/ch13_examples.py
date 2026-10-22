"""Volume 5, Chapter 12 - Four Ways to Design an Algorithm, on the reading club's book budget.

Run:  python3 ch12_examples.py
"""

from __future__ import annotations

import itertools

# The reading club has 20 pounds; each book has a price and a number of members who voted for it.
BOOKS = [("Atlas", 9, 6), ("Novel", 6, 4), ("Poems", 5, 6), ("Comic", 5, 2), ("Cookbook", 10, 7)]
BUDGET = 20


def brute_force(books: list, budget: int) -> tuple[int, tuple, int]:
    """Try every set of books (2^n of them). Returns (votes, names, sets tried)."""
    best, best_set, tried = 0, (), 0
    for k in range(len(books) + 1):
        for combo in itertools.combinations(books, k):
            tried += 1
            if sum(p for _, p, _ in combo) <= budget:
                v = sum(v for *_, v in combo)
                if v > best:
                    best, best_set = v, tuple(n for n, *_ in combo)
    return best, best_set, tried


def greedy(books: list, budget: int, key) -> tuple[int, tuple]:
    """Take books in order of key while they fit. Fast, but not always best."""
    left, votes, chosen = budget, 0, []
    for name, price, v in sorted(books, key=key):
        if price <= left:
            left -= price
            votes += v
            chosen.append(name)
    return votes, tuple(chosen)


def divide_and_conquer_max(values: list) -> int:
    """Divide and conquer on a different question: the most votes any one book got (split, solve, combine)."""
    if len(values) == 1:
        return values[0]
    mid = len(values) // 2
    return max(divide_and_conquer_max(values[:mid]), divide_and_conquer_max(values[mid:]))


def backtracking(books: list, budget: int, check_first: bool = False) -> tuple[int, tuple, int]:
    """Decide each book in turn (take it or not), abandoning any branch that is over budget.
    Every call counts as one branch, including a call that finds itself over budget and stops at once;
    check_first=True tests the price before calling instead, so those calls are never made.
    Returns (votes, names, branches explored)."""
    best = [0, ()]
    explored = [0]

    def go(i, left, votes, chosen):
        explored[0] += 1
        if left < 0:
            return                                    # over budget: give up on this branch at once
        if votes > best[0]:
            best[0], best[1] = votes, tuple(chosen)
        if i == len(books):
            return
        name, price, v = books[i]
        if not check_first or price <= left:
            go(i + 1, left - price, votes + v, chosen + [name])
        go(i + 1, left, votes, chosen)

    go(0, budget, 0, [])
    return best[0], best[1], explored[0]


if __name__ == "__main__":
    print(brute_force(BOOKS, BUDGET))
    print(greedy(BOOKS, BUDGET, key=lambda b: -b[2]), greedy(BOOKS, BUDGET, key=lambda b: b[1]),
          greedy(BOOKS, BUDGET, key=lambda b: -b[2] / b[1]))
    print(divide_and_conquer_max([v for *_, v in BOOKS]))
    print(backtracking(BOOKS, BUDGET))
