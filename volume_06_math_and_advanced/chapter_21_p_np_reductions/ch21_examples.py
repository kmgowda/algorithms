"""Volume 6, Chapter 21 - P, NP, and Reductions: easy to check, hard to find, and problems that turn into each other.

Run:  python3 ch21_examples.py
"""

from __future__ import annotations

import itertools

PRICES = [12, 7, 15, 9, 4, 11, 6, 13, 8, 5]           # book prices; can some of them total exactly the voucher?


def check_subset(prices: list, chosen: list, target: int) -> bool:
    """Checking a proposed answer (a certificate) is fast: add it up (Figure 21.1)."""
    return len(set(chosen)) == len(chosen) and all(0 <= i < len(prices) for i in chosen) and sum(prices[i] for i in chosen) == target


def find_subset(prices: list, target: int) -> tuple[list | None, int]:
    """Finding one by trying subsets: up to 2^n of them. Returns (indices or None, subsets tried)."""
    tried = 0
    for k in range(len(prices) + 1):
        for combo in itertools.combinations(range(len(prices)), k):
            tried += 1
            if sum(prices[i] for i in combo) == target:
                return list(combo), tried
    return None, tried


# Reduction: "is there an independent set of size k in G?" becomes "is there a clique of size k in the complement of G?"
def complement(vertices: list, edges: set) -> set:
    return {(a, b) for a, b in itertools.combinations(vertices, 2) if (a, b) not in edges and (b, a) not in edges}


def has_clique(vertices: list, edges: set, k: int) -> list | None:
    for group in itertools.combinations(vertices, k):
        if all((a, b) in edges or (b, a) in edges for a, b in itertools.combinations(group, 2)):
            return list(group)
    return None


def has_independent_set(vertices: list, edges: set, k: int) -> list | None:
    return has_clique(vertices, complement(vertices, edges), k)       # the whole reduction is one line


TOWN = ["Library", "School", "Park", "Market", "Station", "Museum", "Hospital", "Harbour"]
ROADS = {("Library", "School"), ("Library", "Park"), ("School", "Market"), ("Park", "Market"), ("School", "Station"),
         ("Market", "Station"), ("Market", "Museum"), ("Park", "Hospital"), ("Hospital", "Museum"), ("Station", "Harbour"),
         ("Museum", "Harbour"), ("Station", "Museum")}

if __name__ == "__main__":
    print(check_subset(PRICES, [0, 2, 4], 31), find_subset(PRICES, 31), find_subset(PRICES, 200), 2 ** len(PRICES))
    print(has_independent_set(TOWN, ROADS, 3), has_independent_set(TOWN, ROADS, 4), has_independent_set(TOWN, ROADS, 5))
