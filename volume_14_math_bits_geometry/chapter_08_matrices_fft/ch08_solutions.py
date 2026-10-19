"""Volume 14, Chapter 8 - Solutions to the exercises."""

from __future__ import annotations

from ch08_examples import mat_pow, poly_mul_fft


def tribonacci_matrix(n: int) -> int:
    """Exercise 1 (LeetCode 1137): M^n maps (T2, T1, T0) = (1, 1, 0) to (T(n+2), T(n+1), T(n)) - read the last row."""
    m = mat_pow([[1, 1, 1], [1, 0, 0], [0, 1, 0]], n)
    return m[2][0] + m[2][1]


def count_walks(adj: list[list[int]], start: int, end: int, steps: int) -> int:
    """Exercise 2: (A^k)[i][j] counts walks of exactly k steps from i to j in a graph."""
    return mat_pow(adj, steps)[start][end]


def dice_sum_ways(dice: int, faces: int = 6) -> list[int]:
    """Exercise 3: ways to roll each total with several dice = repeated polynomial multiplication."""
    poly = [1]
    for _ in range(dice):
        poly = poly_mul_fft(poly, [0] + [1] * faces)
    return poly


if __name__ == "__main__":
    print([tribonacci_matrix(n) for n in range(8)], count_walks([[0, 1, 1], [1, 0, 1], [1, 1, 0]], 0, 0, 3),
          dice_sum_ways(2)[7])
