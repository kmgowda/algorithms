"""Volume 2, Chapter 2 - Growth Rates Visualized.

Run:  python3 ch02_examples.py
"""

from __future__ import annotations

import math
from typing import Callable

GROWTH: dict[str, Callable[[int], float]] = {
    "1": lambda n: 1,
    "log n": lambda n: math.log2(n) if n > 1 else 1,
    "n": lambda n: n,
    "n log n": lambda n: n * math.log2(n) if n > 1 else 1,
    "n^2": lambda n: n ** 2,
    "n^3": lambda n: n ** 3,
    "2^n": lambda n: 2 ** n,
    "n!": lambda n: math.factorial(n),
}


def growth_row(n: int) -> dict[str, float]:
    """Steps needed by every growth rate at one input size."""
    return {name: f(n) for name, f in GROWTH.items()}


def ascii_bars(values: dict[str, float], width: int = 40) -> list[str]:
    """Draw values as text bars scaled so the largest bar is `width` characters long."""
    biggest = max(values.values())
    lines = []
    for name, value in values.items():
        length = max(1, round(value / biggest * width)) if value > 0 else 0
        lines.append(f"{name:>8} | {'#' * length} {value:,.0f}")
    return lines


def crossover(slow_start: Callable[[int], float], fast_start: Callable[[int], float],
              limit: int = 10_000_000) -> int | None:
    """Smallest n >= 1 from which `fast_start(n)` is larger than `slow_start(n)` and stays larger.

    Example: 100n starts bigger than n^2, but n^2 overtakes it at n = 101.
    Checked by scanning, then confirmed for a few doublings beyond.
    """
    for n in range(1, limit):
        if fast_start(n) > slow_start(n):
            if all(fast_start(m) > slow_start(m) for m in (2 * n, 4 * n, 8 * n)):
                return n
    return None


def largest_n_within(budget_steps: float, cost: Callable[[int], float]) -> int:
    """Largest n with cost(n) <= budget: double to find an upper bound, then binary search."""
    if cost(1) > budget_steps:
        return 0
    high = 1
    while cost(high) <= budget_steps:
        high *= 2
    low = high // 2                      # cost(low) fits, cost(high) does not
    while low + 1 < high:
        middle = (low + high) // 2
        if cost(middle) <= budget_steps:
            low = middle
        else:
            high = middle
    return low


def users_supported(servers: int, steps_per_server: float, cost: Callable[[int], float]) -> int:
    """Industry example: how many users can a system handle per second if handling n users costs cost(n)?"""
    return largest_n_within(servers * steps_per_server, cost)


def simple_vs_compound(deposit: float, rate_percent: float, years: int) -> tuple[float, float]:
    """Linear growth (simple interest) vs. exponential growth (compound interest)."""
    simple = deposit * (1 + rate_percent / 100 * years)
    compound = deposit * (1 + rate_percent / 100) ** years
    return round(simple, 2), round(compound, 2)


if __name__ == "__main__":
    for line in ascii_bars({k: v for k, v in growth_row(16).items() if k not in ("n!",)}):
        print(line)
    print("100n vs n^2 crossover at n =", crossover(lambda n: 100 * n, lambda n: n * n))
    print("n^3 vs 2^n crossover at n =", crossover(lambda n: n ** 3, lambda n: 2 ** n))
    one_second = 1e9
    for name in ("n", "n log n", "n^2", "n^3", "2^n", "n!"):
        print(f"{name:>8}: largest n in one second = {largest_n_within(one_second, GROWTH[name]):,}")
    print("Savings after 30 years (simple, compound):", simple_vs_compound(1000, 7, 30))
