"""Volume 4, Chapter 30 - Branch and Bound: prune any branch whose best possible result cannot beat the best found.

Run:  python3 ch30_examples.py
"""

from __future__ import annotations

import random

# Chapter 12's books: (name, price, votes); budget 20 pounds, whole books only.
BOOKS = [("Atlas", 9, 6), ("Novel", 6, 4), ("Poems", 5, 6), ("Comic", 5, 2), ("Cookbook", 10, 7)]


def fractional_bound(items: list, i: int, room: float) -> float:
    """The most votes still possible if the remaining items could be bought in part (Chapter 14)."""
    best = 0.0
    for _, price, votes in items[i:]:
        if price <= room:
            room -= price
            best += votes
        else:
            return best + votes * room / price
    return best


def branch_and_bound(books: list, budget: int, use_bound: bool = True, log: list | None = None) -> tuple[int, list, int]:
    """Take-or-leave search in order of votes per pound, cutting branches whose bound cannot beat the best so far.
    Returns (votes, names, nodes visited)."""
    items = sorted(books, key=lambda b: b[2] / b[1], reverse=True)
    best = [0, []]
    nodes = [0]

    def go(i, room, votes, chosen):
        nodes[0] += 1
        if votes > best[0]:
            best[0], best[1] = votes, list(chosen)
        if i == len(items):
            return
        bound = votes + fractional_bound(items, i, room)
        if use_bound and bound <= best[0]:
            if log is not None:
                log.append((i, votes, round(bound, 2), best[0]))
            return                                    # even the optimistic bound cannot beat the best: prune
        name, price, v = items[i]
        if price <= room:
            chosen.append(name)
            go(i + 1, room - price, votes + v, chosen)
            chosen.pop()
        go(i + 1, room, votes, chosen)

    go(0, budget, 0, [])
    return best[0], best[1], nodes[0]


def random_shop(n: int, seed: int) -> list:
    r = random.Random(seed)
    return [(f"b{i}", r.randint(2, 20), r.randint(1, 15)) for i in range(n)]


if __name__ == "__main__":
    log = []
    print(branch_and_bound(BOOKS, 20, True, log), log)
    print(branch_and_bound(BOOKS, 20, False))
    for n in (10, 20, 30):
        shop = random_shop(n, n)
        cap = sum(p for _, p, _ in shop) // 3
        a, b = branch_and_bound(shop, cap, True), branch_and_bound(shop, cap, False) if n <= 20 else (None, None, None)
        print(n, a[0], a[2], b[0], b[2])
