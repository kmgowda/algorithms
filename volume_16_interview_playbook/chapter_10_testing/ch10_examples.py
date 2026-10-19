"""Volume 16, Chapter 10 - Testing, Edge Cases, and Debugging Under Pressure.

Run:  python3 ch10_examples.py
"""

from __future__ import annotations

import random
from typing import Callable


def max_profit_buggy(prices: list[int]) -> int:
    """A plausible-looking one-trade stock solution with a hidden bug: it compares each price only with
    the previous day, instead of with the cheapest day so far."""
    best = 0
    for i in range(1, len(prices)):
        best = max(best, prices[i] - prices[i - 1])
    return best


def max_profit(prices: list[int]) -> int:
    """LeetCode 121, fixed: track the cheapest price seen so far."""
    cheapest, best = float("inf"), 0
    for p in prices:
        cheapest = min(cheapest, p)
        best = max(best, p - cheapest)
    return int(best)


def max_profit_brute(prices: list[int]) -> int:
    """The obviously correct reference: try every buy day and later sell day (or don't trade: profit 0)."""
    return max([0] + [prices[j] - prices[i] for i in range(len(prices)) for j in range(i + 1, len(prices))])


def edge_cases_for_list() -> list[list[int]]:
    """The standard checklist for list inputs."""
    return [[], [5], [5, 5], [1, 2, 3, 4], [4, 3, 2, 1], [3, 1, 3, 1], [0, 10 ** 9], [7, 1, 5, 3, 6, 4]]


def find_counterexample(fast: Callable[[list[int]], int], slow: Callable[[list[int]], int],
                        trials: int, rng: random.Random) -> list[int] | None:
    """Random testing: generate many small inputs and return the first one where the two disagree."""
    for _ in range(trials):
        case = [rng.randint(0, 9) for _ in range(rng.randint(0, 6))]
        if fast(case) != slow(case):
            return case
    return None


def shrink(case: list[int], fails: Callable[[list[int]], bool]) -> list[int]:
    """Make a failing input as small as possible: keep deleting single elements while it still fails."""
    changed = True
    while changed:
        changed = False
        for i in range(len(case)):
            smaller = case[:i] + case[i + 1:]
            if fails(smaller):
                case, changed = smaller, True
                break
    return case


def debug_report(prices: list[int]) -> list[str]:
    """Industry example: print the state at each step - the fastest way to see where a trace goes wrong."""
    lines, cheapest, best = [], float("inf"), 0
    for day, p in enumerate(prices):
        cheapest = min(cheapest, p)
        best = max(best, p - cheapest)
        lines.append(f"day {day}: price {p}, cheapest {cheapest}, best {best}")
    return lines


if __name__ == "__main__":
    rng = random.Random(1)
    print([max_profit_buggy(c) == max_profit_brute(c) for c in edge_cases_for_list()])
    bad = find_counterexample(max_profit_buggy, max_profit_brute, 1000, rng)
    print("counterexample:", bad)
    small = shrink(bad, lambda c: max_profit_buggy(c) != max_profit_brute(c))
    print("shrunk to:", small, max_profit_buggy(small), "vs", max_profit_brute(small))
    print("fixed version agrees:", find_counterexample(max_profit, max_profit_brute, 1000, rng) is None)
    print("\n".join(debug_report([3, 1, 4, 1, 5])))
