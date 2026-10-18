"""Volume 12, Chapter 1 - Remember, Don't Recompute: Memoization.

Run:  python3 ch01_examples.py
"""

from __future__ import annotations

import timeit
from functools import lru_cache


def fib_naive(n: int, counter: list[int] | None = None) -> int:
    """Rabbit pairs after n months (Fibonacci). Plain recursion: fib(n-2) is computed again inside fib(n-1)."""
    if counter is not None:
        counter[0] += 1
    if n < 2:
        return n
    return fib_naive(n - 1, counter) + fib_naive(n - 2, counter)


def fib_memo(n: int, memo: dict[int, int] | None = None) -> int:
    """The same recursion with a notebook: look the answer up before computing it."""
    memo = {} if memo is None else memo
    if n < 2:
        return n
    if n not in memo:
        memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]


@lru_cache(maxsize=None)
def fib_cached(n: int) -> int:
    """Python's built-in notebook: @lru_cache remembers every argument it has seen."""
    return n if n < 2 else fib_cached(n - 1) + fib_cached(n - 2)


def grid_routes_naive(rows: int, cols: int) -> int:
    """Routes from the top-left to the bottom-right moving only right or down. Exponential without memory."""
    if rows == 1 or cols == 1:
        return 1
    return grid_routes_naive(rows - 1, cols) + grid_routes_naive(rows, cols - 1)


def grid_routes_memo(rows: int, cols: int) -> int:
    """Memoized: there are only rows x cols different questions, each answered once."""
    @lru_cache(maxsize=None)
    def routes(r: int, c: int) -> int:
        if r == 1 or c == 1:
            return 1
        return routes(r - 1, c) + routes(r, c - 1)
    return routes(rows, cols)


def distinct_subproblems(n: int) -> tuple[int, int]:
    """How many calls naive Fibonacci makes vs. how many DIFFERENT questions it asks."""
    counter = [0]
    fib_naive(n, counter)
    return counter[0], n + 1


def make_cached_quote(price_lookup):
    """Industry example: wrap an expensive pricing service so repeated questions are answered from memory."""
    calls = [0]

    @lru_cache(maxsize=1024)
    def quote(route: str) -> float:
        calls[0] += 1
        return price_lookup(route)

    return quote, calls


if __name__ == "__main__":
    print("fib(30) calls:", distinct_subproblems(30), "->", fib_memo(30), fib_cached(30))
    t_naive = min(timeit.repeat(lambda: fib_naive(27), number=1, repeat=3))
    t_memo = min(timeit.repeat(lambda: fib_memo(27), number=1, repeat=3))
    print(f"fib(27): naive {t_naive * 1000:.1f} ms, memoized {t_memo * 1000:.3f} ms")
    print("grid 10x10 routes:", grid_routes_naive(10, 10), grid_routes_memo(10, 10), "| 30x30:", grid_routes_memo(30, 30))
    quote, calls = make_cached_quote(lambda route: len(route) * 12.5)
    for r in ["BLR-DEL", "BLR-DEL", "BOM-GOI", "BLR-DEL"]:
        quote(r)
    print("pricing service called", calls[0], "times for 4 requests")
