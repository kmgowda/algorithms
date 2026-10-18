"""Volume 12, Chapter 8 - Solutions to the exercises."""

from __future__ import annotations

from functools import lru_cache


def stone_merge_cost(piles: list[int]) -> int:
    """Exercise 1: merge neighbouring piles two at a time; each merge costs the merged size. Cheapest total?"""
    n = len(piles)
    prefix = [0]
    for p in piles:
        prefix.append(prefix[-1] + p)

    @lru_cache(maxsize=None)
    def best(i: int, j: int) -> int:
        if i == j:
            return 0
        return prefix[j + 1] - prefix[i] + min(best(i, k) + best(k + 1, j) for k in range(i, j))

    return best(0, n - 1) if n else 0


def min_score_triangulation(values: list[int]) -> int:
    """Exercise 2 (LeetCode 1039): split a convex polygon into triangles; a triangle's score is the product of its
    corners. Minimum total? Edge (i, j) belongs to one triangle with some third corner k between them."""
    n = len(values)
    best = [[0] * n for _ in range(n)]
    for gap in range(2, n):
        for i in range(n - gap):
            j = i + gap
            best[i][j] = min(best[i][k] + values[i] * values[k] * values[j] + best[k][j] for k in range(i + 1, j))
    return best[0][n - 1]


def brute_matrix_chain(dims: list[int]) -> int:
    """Exercise 3: try every bracketing recursively, no memo (exponential)."""
    def go(i: int, j: int) -> int:
        if i == j:
            return 0
        return min(go(i, k) + go(k + 1, j) + dims[i - 1] * dims[k] * dims[j] for k in range(i, j))
    return go(1, len(dims) - 1)


if __name__ == "__main__":
    print(stone_merge_cost([4, 1, 2, 3]), min_score_triangulation([3, 7, 4, 5]), brute_matrix_chain([10, 30, 5, 60]))
