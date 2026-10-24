"""Volume 1, Chapter 9 - Best, Worst, and Average Case.

Run:  python3 ch09_examples.py
"""

from __future__ import annotations

SHELF = [12, 25, 31, 47, 58, 63, 70, 84, 91]


def looks(shelf: list[int], target: int) -> int:
    """Looks linear search needs: position + 1 if found, len(shelf) if missing (Figure 9.2)."""
    for i, book in enumerate(shelf):
        if book == target:
            return i + 1
    return len(shelf)


def average_looks(shares: list[float]) -> float:
    """Average looks of linear search when the book at position p (counting from 1) is requested with
    probability shares[p - 1] (Figures 9.3 and 9.4)."""
    return sum(p * s for p, s in enumerate(shares, start=1))


def popularity_first(n: int) -> list[float]:
    """Request shares falling off as 1/p (most popular first), as in Figure 9.4."""
    weights = [1 / p for p in range(1, n + 1)]
    total = sum(weights)
    return [w / total for w in weights]


def harmonic(n: int) -> float:
    """The n-th harmonic number H(n) = 1 + 1/2 + ... + 1/n (Section 9.8; H(9) is about 2.83)."""
    return sum(1 / k for k in range(1, n + 1))


def average_with_misses(n: int, s: float) -> float:
    """Average looks of linear search on n books when the book is on the shelf with probability s (each
    position equally likely) and missing otherwise: s(n + 1)/2 + n(1 - s) (Section 9.5).
    An empty shelf needs no looks at all, so n = 0 gives 0."""
    if n == 0:
        return 0
    return s * (n + 1) / 2 + n * (1 - s)


TALLEST = [142, 155, 138, 161, 150, 158]               # the line of children from Chapter 1


def updates(heights: list) -> int:
    """How many times the tallest-so-far changes after the first child (Chapter 1's algorithm)."""
    best, count = heights[0], 0
    for h in heights[1:]:
        if h > best:
            best, count = h, count + 1
    return count


def average_updates(n: int) -> float:
    """Average of updates over all n! orders of n different heights, by trying them all."""
    import itertools
    orders = list(itertools.permutations(range(n)))
    return sum(updates(list(p)) for p in orders) / len(orders)


if __name__ == "__main__":
    print([looks(SHELF, b) for b in SHELF], looks(SHELF, 50))
    print(average_looks([1 / 9] * 9), round(average_looks(popularity_first(9)), 2))
    print(average_looks([0.5] + [0.5 / 8] * 8))
    print(round(harmonic(9), 2), average_with_misses(9, 0.5), average_with_misses(100, 0.75))
    print(updates(TALLEST), average_updates(6), harmonic(6) - 1)
