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


if __name__ == "__main__":
    print([looks(SHELF, b) for b in SHELF], looks(SHELF, 50))
    print(average_looks([1 / 9] * 9), round(average_looks(popularity_first(9)), 2))
    print(average_looks([0.5] + [0.5 / 8] * 8))
