"""Volume 7, Chapter 33 - Thinking Problems.

Problem 1: largest_input makes O(log n) cost evaluations (doubling, then binary search); counted here.
Problem 2: plan the branch sites within a step budget: exact search if it fits, else the farthest-home rule plus swaps.
Problem 3: judging growth rates at one small n: 50 n log n loses to n^2 below the crossover, wins above it.
"""

from __future__ import annotations

import math

from ch33_examples import GROWTH, exact_sites, exact_steps, greedy_sites, radius, swap_search


def largest_input_counted(rate: str, budget: int) -> tuple[int, int]:
    """largest_input with a count of cost evaluations."""
    f, evals = GROWTH[rate], [0]

    def cost(n):
        evals[0] += 1
        return f(n)
    if cost(1) > budget:
        return 0, evals[0]
    hi = 1
    while cost(hi * 2) <= budget:
        hi *= 2
    lo, hi = hi, hi * 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        lo, hi = (mid, hi) if cost(mid) <= budget else (lo, mid)
    return lo, evals[0]


def plan_sites(sites, homes, k: int, budget: int) -> tuple[str, list, float]:
    """Exact if the exhaustive search fits the budget; otherwise greedy then swap local search."""
    if exact_steps(len(sites), k, len(homes)) <= budget:
        chosen, how = exact_sites(sites, homes, k), "exact"
    else:
        chosen, how = swap_search(greedy_sites(sites, homes, k), sites, homes), "greedy + swaps"
    return how, chosen, radius(chosen, sites, homes)


def crossover(f, g, start: int = 2, limit: int = 10 ** 6) -> int | None:
    """Smallest n >= start at which f(n) < g(n) and stays so up to limit (checked by doubling then scanning)."""
    for n in range(start, limit):
        if f(n) < g(n):
            return n
    return None


if __name__ == "__main__":
    from ch33_examples import town
    print(largest_input_counted("n^2", 10 ** 8), largest_input_counted("n", 10 ** 8))
    s, h = town(12, 200, 30)
    print(plan_sites(s, h, 3, 10 ** 6)[0:2], plan_sites(s, h, 3, 1000)[0:2])
    print(crossover(lambda n: 50 * n * math.log2(n), lambda n: n * n))
