"""Volume 12, Chapter 2 - Top-Down vs. Bottom-Up.

Run:  python3 ch02_examples.py
"""

from __future__ import annotations

import sys
import timeit
from functools import lru_cache


def min_steps_top_down(n: int) -> int:
    """Fewest steps to reduce n to 1 using: subtract 1, halve (if even), divide by 3 (if divisible).
    Top-down: start from the question, recurse on what it needs, remember answers."""
    @lru_cache(maxsize=None)
    def best(k: int) -> int:
        if k == 1:
            return 0
        options = [best(k - 1)]
        if k % 2 == 0:
            options.append(best(k // 2))
        if k % 3 == 0:
            options.append(best(k // 3))
        return 1 + min(options)
    return best(n)


def min_steps_bottom_up(n: int) -> int:
    """Bottom-up: fill a table from the smallest subproblem upward, so every answer needed is already there."""
    dp = [0] * (n + 1)
    for k in range(2, n + 1):
        dp[k] = dp[k - 1] + 1
        if k % 2 == 0:
            dp[k] = min(dp[k], dp[k // 2] + 1)
        if k % 3 == 0:
            dp[k] = min(dp[k], dp[k // 3] + 1)
    return dp[n]


def fib_bottom_up(n: int) -> int:
    """Bottom-up Fibonacci: no recursion, so no recursion-depth limit."""
    if n < 2:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]


def deep_top_down_fails(n: int) -> str:
    """Top-down recursion n levels deep can exceed Python's recursion limit."""
    @lru_cache(maxsize=None)
    def f(k: int) -> int:
        return 0 if k == 0 else f(k - 1) + 1
    try:
        f(n)
        return "ok"
    except RecursionError:
        return f"RecursionError (limit {sys.getrecursionlimit()})"


def sparse_top_down_count(n: int) -> tuple[int, int]:
    """Top-down only visits subproblems the answer actually needs. Returns (answer, subproblems visited)
    for 'fewest steps to 1 using only halve or divide by 3 when possible, else subtract 1'."""
    seen: set[int] = set()

    @lru_cache(maxsize=None)
    def best(k: int) -> int:
        seen.add(k)
        if k == 1:
            return 0
        options = [best(k - 1)] if k % 2 and k % 3 else []
        if k % 2 == 0:
            options.append(best(k // 2))
        if k % 3 == 0:
            options.append(best(k // 3))
        return 1 + min(options)

    return best(n), len(seen)


def race(n: int) -> dict[str, float]:
    return {"top-down": min(timeit.repeat(lambda: min_steps_top_down(n), number=1, repeat=3)),
            "bottom-up": min(timeit.repeat(lambda: min_steps_bottom_up(n), number=1, repeat=3))}


def shipping_cost_table(max_weight: int, rates: dict[int, int]) -> list[int]:
    """Industry example: cheapest cost to ship every weight 0..max_weight using parcel sizes (weight -> price),
    precomputed bottom-up so a website can look any weight up instantly."""
    INF = 10 ** 9
    dp = [0] + [INF] * max_weight
    for w in range(1, max_weight + 1):
        for size, price in rates.items():
            if size <= w and dp[w - size] + price < dp[w]:
                dp[w] = dp[w - size] + price
    return dp


if __name__ == "__main__":
    print("10 -> 1 in", min_steps_top_down(10), min_steps_bottom_up(10), "steps")
    print("fib(500) bottom-up has", len(str(fib_bottom_up(500))), "digits")
    print("top-down 5000 deep:", deep_top_down_fails(5000))
    print("sparse top-down for 10**6:", sparse_top_down_count(10 ** 6))
    print({k: f"{v * 1e6:.0f} us" for k, v in race(400).items()})
    print("shipping 1-10 kg:", shipping_cost_table(10, {1: 60, 2: 100, 5: 220})[1:])
