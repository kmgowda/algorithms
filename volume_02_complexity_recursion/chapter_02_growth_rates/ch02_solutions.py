"""Volume 2, Chapter 2 - Solutions to the exercises."""

from __future__ import annotations

import math

from ch02_examples import crossover, largest_n_within


def rank_by_growth(names: list[str], at_n: int = 1000) -> list[str]:
    """Exercise 1: order growth-rate names from slowest to fastest by evaluating them at a large n."""
    values = {
        "1": 1, "log n": math.log2(at_n), "sqrt n": math.sqrt(at_n), "n": at_n,
        "n log n": at_n * math.log2(at_n), "n^2": at_n ** 2, "n^3": at_n ** 3,
        "2^n": 2.0 ** at_n, "n!": math.inf,
    }
    return sorted(names, key=lambda name: values[name])


def crossover_constant_vs_quadratic() -> int | None:
    """Exercise 2: from which n is 2n^2 bigger than 50n + 1000?"""
    return crossover(lambda n: 50 * n + 1000, lambda n: 2 * n * n)


def bacteria_hours(start: int, target: int) -> int:
    """Exercise 3: bacteria double every hour. Hours until there are at least `target`."""
    hours, count = 0, start
    while count < target:
        count *= 2
        hours += 1
    return hours


def fits_in_budget(budget: float) -> dict[str, int]:
    """Exercise 4: largest n for each growth rate within a budget of steps."""
    return {
        "n": largest_n_within(budget, lambda n: n),
        "n^2": largest_n_within(budget, lambda n: n * n),
        "2^n": largest_n_within(budget, lambda n: 2 ** n),
    }


def faster_computer_gain(speedup: float) -> dict[str, float]:
    """Exercise 5: with a computer `speedup` times faster, how much bigger an input fits in the same time?"""
    return {
        "n": speedup,                    # n grows by the full factor
        "n^2": math.sqrt(speedup),       # n grows by the square root
        "2^n": math.log2(speedup),       # n grows by a fixed ADDED amount
    }


if __name__ == "__main__":
    print(rank_by_growth(["n^2", "log n", "2^n", "n", "1", "n log n"]))
    print(crossover_constant_vs_quadratic(), bacteria_hours(1, 1_000_000))
    print(fits_in_budget(1e6), faster_computer_gain(100))
