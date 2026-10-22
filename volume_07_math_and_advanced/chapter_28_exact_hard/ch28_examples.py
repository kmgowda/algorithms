"""Volume 7, Chapter 28 - Exact Algorithms for Hard Problems: smarter exponential searches.

Run:  python3 ch28_examples.py
"""

from __future__ import annotations

import bisect
import itertools
import random

TOWN = ["Library", "School", "Park", "Market", "Station", "Museum", "Hospital", "Harbour"]
ROADS = [("Library", "School"), ("Library", "Park"), ("School", "Market"), ("Park", "Market"), ("School", "Station"),
         ("Market", "Station"), ("Market", "Museum"), ("Park", "Hospital"), ("Hospital", "Museum"), ("Station", "Harbour"),
         ("Museum", "Harbour"), ("Station", "Museum")]


def cover_branching(edges: list, k: int, calls: list) -> list | None:
    """Vertex cover of size at most k (Figure 28.2): any uncovered road needs one of its two ends, so try each.
    At most 2^k branches, however many places there are."""
    calls[0] += 1
    if not edges:
        return []
    if k == 0:
        return None
    a, b = edges[0]
    for v in (a, b):
        rest = cover_branching([e for e in edges if v not in e], k - 1, calls)
        if rest is not None:
            return [v] + rest
    return None


def cover_brute(vertices: list, edges: list, k: int) -> tuple[list | None, int]:
    tried = 0
    for size in range(k + 1):
        for g in itertools.combinations(vertices, size):
            tried += 1
            if all(a in g or b in g for a, b in edges):
                return list(g), tried
    return None, tried


def subset_sum_mitm(values: list, target: int) -> tuple[bool, int]:
    """Meet in the middle (Figure 28.3): all sums of each half (2^(n/2) each), sort one, look up the other.
    Returns (found?, sums listed)."""
    half = len(values) // 2
    left, right = values[:half], values[half:]
    sums = lambda vs: [sum(c) for k in range(len(vs) + 1) for c in itertools.combinations(vs, k)]
    ls, rs = sums(left), sorted(sums(right))
    for s in ls:
        i = bisect.bisect_left(rs, target - s)
        if i < len(rs) and rs[i] == target - s:
            return True, len(ls) + len(rs)
    return False, len(ls) + len(rs)


def subset_sum_mitm_trace(values: list, target: int) -> tuple[list, list, tuple | None]:
    """The two half-lists for a hand trace: (left sums, sorted right sums, the matching pair or None)."""
    half = len(values) // 2
    sums = lambda vs: sorted({sum(c) for k in range(len(vs) + 1) for c in itertools.combinations(vs, k)})
    ls, rs = sums(values[:half]), sums(values[half:])
    for s_ in ls:
        i = bisect.bisect_left(rs, target - s_)
        if i < len(rs) and rs[i] == target - s_:
            return ls, rs, (s_, rs[i])
    return ls, rs, None


# ---------------------------------------------------------------- kernelisation (Buss)

def buss_kernel(edges: list, k: int) -> tuple[list | None, list, int]:
    """Shrink a vertex-cover instance (Figure 28.3): a place with more than k roads must be in any cover of size k
    (otherwise all its more-than-k neighbours would be needed); take it, delete its roads, lower k. Afterwards, if
    more than k^2 roads remain, no cover of size k exists. Returns (remaining roads or None if impossible,
    forced places, remaining k)."""
    edges, forced = list(edges), []
    changed = True
    while changed and k >= 0:
        changed = False
        deg = {}
        for a, b in edges:
            deg[a] = deg.get(a, 0) + 1
            deg[b] = deg.get(b, 0) + 1
        for v, dv in sorted(deg.items()):
            if dv > k:
                forced.append(v)
                edges = [e for e in edges if v not in e]
                k -= 1
                changed = True
                break
    if k < 0 or len(edges) > k * k:
        return None, forced, k
    return edges, forced, k


def cover_with_kernel(edges: list, k: int) -> list | None:
    kernel, forced, k2 = buss_kernel(edges, k)
    if kernel is None:
        return None
    rest = cover_branching(kernel, k2, [0])
    return None if rest is None else forced + rest


def cover_branching_better(edges: list, k: int, calls: list) -> list | None:
    """The refined branching: if some place v has 3 or more uncovered roads, either v is in the cover, or all its
    neighbours are (at least 3 places at once). Otherwise every place has at most 2 roads, and branching on a road
    is cheap. Search tree about 1.47^k instead of 2^k."""
    calls[0] += 1
    if not edges:
        return []
    if k <= 0:
        return None
    deg = {}
    for a, b in edges:
        deg.setdefault(a, set()).add(b)
        deg.setdefault(b, set()).add(a)
    v = max(sorted(deg), key=lambda x: len(deg[x]))
    if len(deg[v]) >= 3:
        rest = cover_branching_better([e for e in edges if v not in e], k - 1, calls)
        if rest is not None:
            return [v] + rest
        nbrs = sorted(deg[v])
        if len(nbrs) <= k:
            rest = cover_branching_better([e for e in edges if e[0] not in nbrs and e[1] not in nbrs], k - len(nbrs), calls)
            if rest is not None:
                return nbrs + rest
        return None
    return cover_branching(edges, k, calls)


# ---------------------------------------------------------------- branch and bound for knapsack

def knapsack_branch_and_bound(values: list, weights: list, cap: int) -> tuple[int, list, int]:
    """Best-first is the textbook choice; this is depth-first branch and bound (Figure 28.4): decide each book in or
    out, in order of value per width, and abandon a branch when even the fractional (greedy) bound cannot beat the
    best answer found so far. Returns (best value, chosen indices, nodes explored)."""
    order = sorted(range(len(values)), key=lambda i: -values[i] / weights[i])
    best = [0, []]
    nodes = [0]

    def bound(i, value, room):
        for j in order[i:]:
            if weights[j] <= room:
                room -= weights[j]
                value += values[j]
            else:
                return value + values[j] * room / weights[j]
        return value

    def go(i, value, room, chosen):
        nodes[0] += 1
        if value > best[0]:
            best[0], best[1] = value, list(chosen)
        if i == len(order) or bound(i, value, room) <= best[0]:
            return
        j = order[i]
        if weights[j] <= room:
            go(i + 1, value + values[j], room - weights[j], chosen + [j])
        go(i + 1, value, room, chosen)
    go(0, 0, cap, [])
    return best[0], sorted(best[1]), nodes[0]


SHELF_VALUES = [602, 1012, 845, 377, 1430, 950, 288, 1199, 733, 516]
SHELF_WEIGHTS = [3, 6, 5, 2, 8, 6, 2, 7, 4, 3]


# ---------------------------------------------------------------- DPLL satisfiability

def dpll(clauses: list, assignment: dict | None = None, stats: dict | None = None) -> dict | None:
    """Davis-Putnam-Logemann-Loveland (Figure 28.5): simplify by unit clauses (a clause with one literal left forces
    it) and pure literals (a variable appearing with one sign only can be set that way), then branch on a variable,
    backtracking on a contradiction. Clauses are lists of +v / -v."""
    assignment = dict(assignment or {})
    stats = stats if stats is not None else {}
    stats.setdefault("decisions", 0)
    stats.setdefault("units", 0)

    def simplify(cls, lit):
        out = []
        for c in cls:
            if lit in c:
                continue
            nc = [l for l in c if l != -lit]
            if not nc:
                return None
            out.append(nc)
        return out

    while True:
        unit = next((c[0] for c in clauses if len(c) == 1), None)
        if unit is None:
            lits = {l for c in clauses for l in c}
            pure = next((l for l in sorted(lits, key=abs) if -l not in lits), None)
            if pure is None:
                break
            unit = pure
        else:
            stats["units"] += 1
        assignment[abs(unit)] = unit > 0
        clauses = simplify(clauses, unit)
        if clauses is None:
            return None
    if not clauses:
        return assignment
    v = abs(clauses[0][0])
    for lit in (v, -v):
        stats["decisions"] += 1
        nc = simplify(clauses, lit)
        if nc is not None:
            result = dpll(nc, {**assignment, v: lit > 0}, stats)
            if result is not None:
                return result
    return None


def brute_sat(clauses: list, n: int) -> bool:
    return any(all(any(bits[abs(l) - 1] == (l > 0) for l in c) for c in clauses) for bits in itertools.product([False, True], repeat=n))


def random_3sat(n: int, m: int, rng) -> list:
    return [[rng.choice([1, -1]) * v for v in rng.sample(range(1, n + 1), 3)] for _ in range(m)]


if __name__ == "__main__":
    c = [0]
    print(cover_branching(ROADS, 4, c), c[0], cover_brute(TOWN, ROADS, 4))
    c = [0]
    print(cover_branching(ROADS, 3, c), c[0])
    r = random.Random(25)
    vals = [r.randint(1, 10 ** 6) for _ in range(24)]
    target = sum(vals[::3])
    print(subset_sum_mitm(vals, target), subset_sum_mitm(vals, 1), 2 ** 24)
    print(subset_sum_mitm_trace([12, 7, 15, 9], 31))
    print(buss_kernel(ROADS, 4), buss_kernel(ROADS, 2), cover_with_kernel(ROADS, 4))
    star = [("hub", f"leaf{i}") for i in range(30)] + [("a", "b"), ("b", "c")]
    print(buss_kernel(star, 3), cover_with_kernel(star, 3))
    c1, c2 = [0], [0]
    print(cover_branching(ROADS, 4, c1), c1[0], cover_branching_better(ROADS, 4, c2), c2[0])
    print(knapsack_branch_and_bound(SHELF_VALUES, SHELF_WEIGHTS, 20), 2 ** 10)
    st = {}
    f = random_3sat(30, 120, random.Random(9))
    res = dpll(f, stats=st)
    print(res is not None, st, all(any(res.get(abs(l), False) == (l > 0) for l in c) for c in f) if res else None)
