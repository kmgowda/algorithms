"""Volume 10, Chapter 6 - Solutions to the exercises."""

from __future__ import annotations

import random

from ch06_examples import knapsack_best, knapsack_greedy


def find_knapsack_counterexample(seed: int = 0, tries: int = 2000) -> tuple[list, int, int, int] | None:
    """Exercise 1: search random small inputs for one where greedy-by-density loses. Returns (items, cap, greedy, best)."""
    rng = random.Random(seed)
    for _ in range(tries):
        items = [(f"i{k}", rng.randint(1, 6), rng.randint(1, 20)) for k in range(rng.randint(2, 4))]
        cap = rng.randint(1, 10)
        g, b = knapsack_greedy(items, cap), knapsack_best(items, cap)
        if g < b:
            return items, cap, g, b
    return None


def coin_counterexample(coins: list[int]) -> int | None:
    """Exercise 2: smallest amount where largest-coin-first uses more coins than necessary."""
    limit = 2 * max(coins)
    best = [0] + [10 ** 9] * limit
    for a in range(1, limit + 1):
        best[a] = min((best[a - c] + 1 for c in coins if c <= a), default=10 ** 9)
        rest, count = a, 0
        for c in sorted(coins, reverse=True):
            count += rest // c
            rest %= c
        if rest == 0 and count > best[a]:
            return a
    return None


def best_of_two_knapsack(items: list[tuple[str, int, int]], capacity: int) -> int:
    """Exercise 3: a classic fix - take the better of greedy and the single most valuable item that fits.
    This is guaranteed to reach at least HALF the optimum."""
    single = max((v for _, w, v in items if w <= capacity), default=0)
    return max(knapsack_greedy(items, capacity), single)


if __name__ == "__main__":
    print(find_knapsack_counterexample())
    print(coin_counterexample([1, 3, 4]), coin_counterexample([1, 5, 10, 25]), coin_counterexample([1, 7, 10]))
    print(best_of_two_knapsack([("small", 1, 2), ("big", 10, 10)], 10))
