"""Volume 7, Chapter 18 - Randomized Algorithms: random choices that make bad cases unlikely (Las Vegas)
or answers almost certainly right (Monte Carlo).

Run:  python3 ch18_examples.py
"""

from __future__ import annotations

import random


def quickselect(values: list, k: int, rng, pivot: str = "random") -> tuple:
    """The k-th smallest (k from 0), counting comparisons. pivot = 'first' or 'random' (Figure 18.1)."""
    if not 0 <= k < len(values):
        raise ValueError("k must be at least 0 and below the number of values")
    a, comparisons = list(values), 0
    while True:
        p = a[0] if pivot == "first" else a[rng.randrange(len(a))]
        less = [x for x in a if x < p]
        equal = [x for x in a if x == p]
        comparisons += len(a)
        if k < len(less):
            a = less
        elif k < len(less) + len(equal):
            return p, comparisons
        else:
            k -= len(less) + len(equal)
            a = [x for x in a if x > p]


def matmul(A, B):
    return [[sum(A[i][t] * B[t][j] for t in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def freivalds(A, B, C, rounds: int, rng) -> bool:
    """Monte Carlo check of A x B = C (Section 18.6): multiply by a random 0/1 vector instead of multiplying matrices.
    A 'no' is certain; a 'yes' is wrong with probability at most 1/2 per round."""
    n = len(A)
    for _ in range(rounds):
        r = [rng.randrange(2) for _ in range(n)]
        Br = [sum(B[i][j] * r[j] for j in range(n)) for i in range(n)]
        ABr = [sum(A[i][j] * Br[j] for j in range(n)) for i in range(n)]
        Cr = [sum(C[i][j] * r[j] for j in range(n)) for i in range(n)]
        if ABr != Cr:
            return False
    return True


# ---------------------------------------------------------------- the probability toolkit

def fixed_points_exact(n: int) -> tuple:
    """Average number of items left in their own place, over all n! orders: exactly 1 (linearity of expectation)."""
    import itertools
    from fractions import Fraction
    perms = list(itertools.permutations(range(n)))
    total = sum(sum(1 for i, x in enumerate(p) if i == x) for p in perms)
    return Fraction(total, len(perms)), len(perms)


def fixed_points_simulated(n: int, trials: int, seed: int) -> float:
    rng = random.Random(seed)
    total = 0
    for _ in range(trials):
        a = list(range(n))
        rng.shuffle(a)
        total += sum(1 for i, x in enumerate(a) if i == x)
    return total / trials


def heads_tail(n: int, at_least: int) -> float:
    """Exact chance that n fair coins show at least `at_least` heads."""
    import math
    return sum(math.comb(n, k) for k in range(at_least, n + 1)) / 2 ** n


def tail_bounds(n: int, share: float) -> dict:
    """For X = heads in n fair coins and a = share x n: Markov P(X >= a) <= E[X] / a; Chebyshev
    P(|X - n/2| >= a - n/2) <= Var / (a - n/2)^2; Chernoff-Hoeffding P(X >= a) <= exp(-2 n (share - 1/2)^2)."""
    import math
    a = share * n
    mean, var, dev = n / 2, n / 4, a - n / 2
    return {"exact": heads_tail(n, math.ceil(a)), "markov": mean / a, "chebyshev": min(1.0, var / dev ** 2),
            "chernoff": math.exp(-2 * n * (share - 0.5) ** 2)}


def trials_until_success(p: float, runs: int, seed: int) -> float:
    """Average number of independent tries with success chance p until the first success (expected 1/p)."""
    rng = random.Random(seed)
    total = 0
    for _ in range(runs):
        k = 1
        while rng.random() >= p:
            k += 1
        total += k
    return total / runs


# ---------------------------------------------------------------- Karger's minimum cut

def karger_once(vertices: list, edges: list, rng) -> tuple[int, set]:
    """One run of Karger's contraction (Figure 18.3): pick random edges and merge their ends, skipping edges inside
    a merged group, until two groups remain. Returns (edges crossing the two groups, one group)."""
    parent = {v: v for v in vertices}

    def find(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    order = list(edges)
    rng.shuffle(order)                    # contracting edges in a random order = picking uniformly among the remaining ones
    groups = len(vertices)
    for a, b in order:
        if groups == 2:
            break
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
            groups -= 1
    cut = sum(1 for a, b in edges if find(a) != find(b))
    side = {v for v in vertices if find(v) == find(vertices[0])}
    return cut, side


def karger(vertices: list, edges: list, runs: int, seed: int) -> tuple[int, int]:
    """Best cut over many runs, and how many runs found it."""
    rng = random.Random(seed)
    results = [karger_once(vertices, edges, rng)[0] for _ in range(runs)]
    best = min(results)
    return best, results.count(best)


def min_cut_brute(vertices: list, edges: list) -> int:
    import itertools
    n, best = len(vertices), None
    first, rest = vertices[0], vertices[1:]
    for k in range(0, n - 1):
        for group in itertools.combinations(rest, k):
            side = {first, *group}
            cut = sum(1 for a, b in edges if (a in side) != (b in side))
            best = cut if best is None else min(best, cut)
    return best


TOWN = ["Library", "School", "Park", "Market", "Station", "Museum", "Hospital", "Harbour"]
ROADS = [("Library", "School"), ("Library", "Park"), ("School", "Market"), ("Park", "Market"), ("School", "Station"),
         ("Market", "Station"), ("Market", "Museum"), ("Park", "Hospital"), ("Hospital", "Museum"), ("Station", "Harbour"),
         ("Museum", "Harbour"), ("Station", "Museum")]


# Two reading rooms, each a group of four desks all wired to each other, joined by two cables (Figure 18.3).
ROOMS = ["A1", "A2", "A3", "A4", "B1", "B2", "B3", "B4"]
CABLES = [(a, b) for g in ("A", "B") for i, a in enumerate([f"{g}{k}" for k in range(1, 5)]) for b in [f"{g}{k}" for k in range(i + 2, 5)]] \
    + [("A1", "B1"), ("A4", "B4")]


if __name__ == "__main__":
    rng = random.Random(18)
    pile = [58, 25, 91, 12, 70, 47, 84, 31, 63]
    print(quickselect(pile, 4, rng), quickselect(pile, 4, rng, "first"))
    sorted_list = list(range(2000))
    print(quickselect(sorted_list, 1000, rng, "first")[1], quickselect(sorted_list, 1000, rng)[1])
    A = [[1, 2], [3, 4]]; B = [[5, 6], [7, 8]]; C = matmul(A, B); bad = [[19, 22], [43, 51]]
    print(C, freivalds(A, B, C, 10, rng), freivalds(A, B, bad, 10, rng))
    fooled = sum(freivalds(A, B, bad, 1, random.Random(s)) for s in range(1000))
    print(fooled)
    print(fixed_points_exact(5), round(fixed_points_simulated(10, 20000, 3), 3))
    for n in (100, 1000):
        print(n, {k: f"{v:.3g}" for k, v in tail_bounds(n, 0.6).items()})
    print(round(trials_until_success(0.25, 20000, 4), 3), round(trials_until_success(1 / 690, 2000, 5), 1))
    print(min_cut_brute(TOWN, ROADS), karger(TOWN, ROADS, 1000, 6), round(2 / (8 * 7), 4))
    rng2 = random.Random(7)
    print(karger_once(TOWN, ROADS, rng2))
    print(len(CABLES), min_cut_brute(ROOMS, CABLES), karger(ROOMS, CABLES, 1000, 8), min(sum(1 for e in CABLES if v in e) for v in ROOMS))
