"""Volume 12, Chapter 1 - Solutions to the exercises."""

from __future__ import annotations

from functools import lru_cache


def tribonacci(n: int) -> int:
    """Exercise 1 (LeetCode 1137): each term is the sum of the previous three."""
    @lru_cache(maxsize=None)
    def t(k: int) -> int:
        if k == 0:
            return 0
        if k <= 2:
            return 1
        return t(k - 1) + t(k - 2) + t(k - 3)
    return t(n)


def tile_ways(n: int) -> int:
    """Exercise 2: ways to cover a 2 x n path with 1 x 2 tiles (vertical, or two horizontal stacked)."""
    @lru_cache(maxsize=None)
    def ways(k: int) -> int:
        if k <= 1:
            return 1
        return ways(k - 1) + ways(k - 2)
    return ways(n)


def binomial(n: int, k: int) -> int:
    """Exercise 3: C(n, k) by Pascal's rule C(n, k) = C(n-1, k-1) + C(n-1, k), memoized."""
    @lru_cache(maxsize=None)
    def c(a: int, b: int) -> int:
        if b == 0 or b == a:
            return 1
        return c(a - 1, b - 1) + c(a - 1, b)
    return c(n, k)


def collatz_steps(n: int, memo: dict[int, int] = {1: 0}) -> int:  # noqa: B006 - shared memo on purpose
    """Exercise 4: steps to reach 1 in the 3n+1 game; a shared memo speeds up many queries."""
    if n not in memo:
        memo[n] = 1 + collatz_steps(n // 2 if n % 2 == 0 else 3 * n + 1)
    return memo[n]


if __name__ == "__main__":
    print(tribonacci(25), tile_ways(10), binomial(30, 15), max(range(1, 10000), key=collatz_steps))
