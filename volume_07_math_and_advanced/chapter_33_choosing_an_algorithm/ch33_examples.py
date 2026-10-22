"""Volume 7, Chapter 33 - The Road Ahead: Choosing an Algorithm (the series in one decision guide).

Run:  python3 ch33_examples.py
"""

from __future__ import annotations

import itertools
import math
import random

GROWTH = {"n": lambda n: n, "n log n": lambda n: n * math.log2(max(n, 2)), "n^2": lambda n: n ** 2, "n^3": lambda n: n ** 3,
          "2^n": lambda n: 2 ** n, "n!": lambda n: math.factorial(n)}


def largest_input(rate: str, budget: int) -> int:
    """The largest n whose cost fits the budget of steps (Figure 33.1), by doubling then binary search."""
    f = GROWTH[rate]
    if f(1) > budget:
        return 0
    hi = 1
    while f(hi * 2) <= budget:
        hi *= 2
    lo, hi = hi, hi * 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        lo, hi = (mid, hi) if f(mid) <= budget else (lo, mid)
    return lo


def fastest_fitting(n: int, budget: int) -> list:
    """Every growth rate whose cost for n items fits the budget."""
    return [rate for rate, f in GROWTH.items() if n == 0 or f(n) <= budget]


RULES = [  # (question, answer, where in the series)
    ("data changes and you search it often", "a hash table or balanced tree", "Volumes 2 and 3"),
    ("range totals or minimums over an array", "prefix sums, Fenwick or segment trees, sparse tables", "Volume 3, Part II"),
    ("you need the order of the data", "sort it", "Volume 4, Part II"),
    ("reachability or fewest hops in a network", "breadth-first or depth-first search", "Volume 4, Part III"),
    ("routes on a map with weights", "Dijkstra, or Bellman-Ford with negative roads", "Volume 5, Part I"),
    ("best choice looks safe at each step and you can prove it", "greedy", "Volume 5, Part II"),
    ("halves independent combine", "divide and conquer", "Volume 5, Part III"),
    ("every possibility with rules to prune", "backtracking, branch and bound", "Volume 6, Part I"),
    ("sub-problems repeat", "dynamic programming", "Volume 6, Part II"),
    ("searching text", "KMP, Horspool, Aho-Corasick, or a suffix array", "Volume 6, Part III"),
    ("divisors primes remainders keys", "Euclid, sieves, fast powers, Miller-Rabin", "Volume 7, Part I"),
    ("points lines polygons", "turn tests, sweeps, hulls", "Volume 7, Part III"),
    ("the problem is NP-hard", "approximate, search locally, or solve small cases exactly", "Volume 7, Part V"),
    ("the data is too big to store", "stream with sketches, or spread it with MapReduce", "Volume 7, Part VI"),
]
_STOP = {"the", "a", "and", "you", "it", "is", "to", "of", "with", "on", "at", "each", "or", "in", "over", "an", "can"}


def advise(situation: str) -> list:
    """Every rule sharing a meaningful word with the situation; [] means think from first principles."""
    words = set(situation.lower().split()) - _STOP
    return [(a, where) for q, a, where in RULES if words & set(q.split())]


def hard_problem_plan(n: int, budget: int, small_parameter: int | None = None, need_proof_of_quality: bool = True) -> str:
    """Section 33.6: the Part V route for an NP-hard problem."""
    if 2 ** n <= budget:
        return "exact: try every subset (or branch and bound)"
    if 2 ** (n / 2) * n <= budget:
        return "exact: meet in the middle"
    if small_parameter is not None and 2 ** small_parameter * n <= budget:
        return "exact: fixed-parameter search"
    if need_proof_of_quality:
        return "approximation with a proven ratio"
    return "local search"


def big_data_plan(fits_in_memory: bool, one_pass_only: bool, machines: int, approximate_ok: bool) -> str:
    """Section 33.7: the Part VI route when data is large."""
    if fits_in_memory:
        return "ordinary in-memory algorithm"
    if one_pass_only:
        return "streaming sketch" if approximate_ok else "streaming exact count (if the keys fit)"
    if machines > 1:
        return "MapReduce"
    return "external sorting"


# ---- the branch-sites worked problem (Section 33.9) -------------------------------------------------------

def town(sites: int = 20, homes: int = 400, seed: int = 30):
    rng = random.Random(seed)
    return ([(rng.uniform(0, 10), rng.uniform(0, 10)) for _ in range(sites)],
            [(rng.uniform(0, 10), rng.uniform(0, 10)) for _ in range(homes)])


def radius(chosen, sites, homes) -> float:
    """The longest walk from any home to its nearest chosen site."""
    return max(min(math.dist(h, sites[s]) for s in chosen) for h in homes)


def greedy_sites(sites, homes, k: int) -> list:
    """Farthest-home rule: open the site nearest the home farthest from every open site (within 3 times the best)."""
    chosen = [min(range(len(sites)), key=lambda s: math.dist(homes[0], sites[s]))]
    while len(chosen) < k:
        far = max(homes, key=lambda h: min(math.dist(h, sites[s]) for s in chosen))
        best = min((s for s in range(len(sites)) if s not in chosen), key=lambda s: math.dist(far, sites[s]))
        chosen.append(best)
    return sorted(chosen)


def swap_search(chosen, sites, homes) -> list:
    """Local search: swap one open site for a closed one while the radius drops."""
    chosen = list(chosen)
    improved = True
    while improved:
        improved = False
        current = radius(chosen, sites, homes)
        for i in range(len(chosen)):
            for s in range(len(sites)):
                if s in chosen:
                    continue
                trial = chosen[:i] + [s] + chosen[i + 1:]
                r = radius(trial, sites, homes)
                if r < current - 1e-12:
                    chosen, current, improved = trial, r, True
    return sorted(chosen)


def exact_sites(sites, homes, k: int) -> list:
    """Try every choice of k sites."""
    return sorted(min(itertools.combinations(range(len(sites)), k), key=lambda c: radius(c, sites, homes)))


def exact_steps(sites: int, k: int, homes: int) -> int:
    """Distance computations for the exhaustive search: every choice, every home, every chosen site."""
    return math.comb(sites, k) * homes * k


if __name__ == "__main__":
    for rate in GROWTH:
        print(rate, largest_input(rate, 10 ** 8))
    print(advise("sub-problems repeat"), advise("too big to store"))
    print(exact_steps(40, 5, 10_000))
    s, h = town()
    g = greedy_sites(s, h, 3)
    l = swap_search(g, s, h)
    e = exact_sites(s, h, 3)
    print(g, round(radius(g, s, h), 2), l, round(radius(l, s, h), 2), e, round(radius(e, s, h), 2), exact_steps(20, 3, 400))
