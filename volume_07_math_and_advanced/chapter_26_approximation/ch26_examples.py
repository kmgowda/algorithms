"""Volume 7, Chapter 26 - Approximation Algorithms: fast answers with a proven bound on how far from best they can be.

Run:  python3 ch26_examples.py
"""

from __future__ import annotations

import itertools
import random

TOWN = ["Library", "School", "Park", "Market", "Station", "Museum", "Hospital", "Harbour"]
ROADS = [("Library", "School"), ("Library", "Park"), ("School", "Market"), ("Park", "Market"), ("School", "Station"),
         ("Market", "Station"), ("Market", "Museum"), ("Park", "Hospital"), ("Hospital", "Museum"), ("Station", "Harbour"),
         ("Museum", "Harbour"), ("Station", "Museum")]


def cover_by_matching(edges: list) -> list:
    """2-approximation for vertex cover (Figure 26.1): take both ends of any road not yet covered."""
    cover = []
    for a, b in edges:
        if a not in cover and b not in cover:
            cover += [a, b]
    return cover


def smallest_cover(vertices: list, edges: list) -> list:
    for k in range(len(vertices) + 1):
        for g in itertools.combinations(vertices, k):
            if all(a in g or b in g for a, b in edges):
                return list(g)


def first_fit_decreasing(sizes: list, capacity: int) -> list:
    """Bin packing: largest box first, into the first bin with room (Figure 26.3). Uses at most about 11/9 of the best."""
    bins = []
    for s in sorted(sizes, reverse=True):
        if s > capacity:
            raise ValueError("a box is larger than a bin")
        for b in bins:
            if sum(b) + s <= capacity:
                b.append(s)
                break
        else:
            bins.append([s])
    return bins


def fewest_bins(sizes: list, capacity: int) -> int:
    for k in range(1, len(sizes) + 1):
        for assign in itertools.product(range(k), repeat=len(sizes)):
            load = [0] * k
            for s, b in zip(sizes, assign):
                load[b] += s
            if max(load) <= capacity:
                return k
    return 0


# ---------------------------------------------------------------- metric TSP: tree doubling and Christofides

TIMED = [("Library", "School", 4), ("Library", "Park", 3), ("School", "Market", 5), ("Park", "Market", 4),
         ("School", "Station", 9), ("Market", "Station", 3), ("Market", "Museum", 6), ("Park", "Hospital", 5),
         ("Hospital", "Museum", 4), ("Station", "Harbour", 6), ("Museum", "Harbour", 3), ("Station", "Museum", 4)]


def travel_times(vertices: list, roads: list) -> dict:
    """Shortest travel minutes between every pair (Floyd-Warshall, Volume 5): these obey the triangle rule."""
    INF = float("inf")
    d = {(a, b): (0 if a == b else INF) for a in vertices for b in vertices}
    for a, b, w in roads:
        d[a, b] = d[b, a] = min(d[a, b], w)
    for k in vertices:
        for i in vertices:
            for j in vertices:
                if d[i, k] + d[k, j] < d[i, j]:
                    d[i, j] = d[i, k] + d[k, j]
    return d


def tour_length(tour: list, d: dict) -> float:
    return sum(d[tour[i], tour[(i + 1) % len(tour)]] for i in range(len(tour)))


def best_tour(vertices: list, d: dict) -> tuple[float, list]:
    first = vertices[0]
    best = None
    for rest in itertools.permutations(vertices[1:]):
        t = [first, *rest]
        L = tour_length(t, d)
        if best is None or L < best[0]:
            best = (L, t)
    return best


def mst(vertices: list, d: dict) -> tuple[list, float]:
    """Prim's minimum spanning tree (Volume 5) on the complete graph of travel times. Returns (edges, weight)."""
    inside, edges, total = {vertices[0]}, [], 0
    while len(inside) < len(vertices):
        a, b = min(((a, b) for a in inside for b in vertices if b not in inside), key=lambda e: d[e])
        inside.add(b)
        edges.append((a, b))
        total += d[a, b]
    return edges, total


def tree_doubling_tour(vertices: list, d: dict) -> tuple[list, float, float]:
    """2-approximation (Figure 26.5): walk round the MST (each edge twice), skipping places already visited.
    Returns (tour, its length, the MST weight)."""
    edges, w = mst(vertices, d)
    adj = {v: [] for v in vertices}
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    tour, seen = [], set()

    def visit(v):
        seen.add(v)
        tour.append(v)
        for u in adj[v]:
            if u not in seen:
                visit(u)
    visit(vertices[0])
    return tour, tour_length(tour, d), w


def christofides(vertices: list, d: dict) -> tuple[list, float]:
    """1.5-approximation: MST plus a cheapest perfect matching on its odd-degree places, an Euler tour of the
    union, then shortcuts. The matching is found by brute force here (fine for small maps)."""
    edges, _ = mst(vertices, d)
    deg = {v: 0 for v in vertices}
    for a, b in edges:
        deg[a] += 1
        deg[b] += 1
    odd = [v for v in vertices if deg[v] % 2]

    def best_matching(nodes):
        if not nodes:
            return 0, []
        a = nodes[0]
        best = None
        for i in range(1, len(nodes)):
            b = nodes[i]
            w, m = best_matching(nodes[1:i] + nodes[i + 1:])
            if best is None or w + d[a, b] < best[0]:
                best = (w + d[a, b], m + [(a, b)])
        return best
    _, matching = best_matching(odd)
    multi = edges + matching
    adj = {v: [] for v in vertices}
    for a, b in multi:
        adj[a].append(b)
        adj[b].append(a)
    stack, circuit = [vertices[0]], []                 # Hierholzer's Euler tour (Volume 5)
    while stack:
        v = stack[-1]
        if adj[v]:
            u = adj[v].pop()
            adj[u].remove(v)
            stack.append(u)
        else:
            circuit.append(stack.pop())
    tour, seen = [], set()
    for v in circuit:
        if v not in seen:
            seen.add(v)
            tour.append(v)
    return tour, tour_length(tour, d)


def no_triangle_instance(vertices: list, roads: list, ratio: float) -> dict:
    """The inapproximability gadget: roads cost 1, non-roads cost ratio x n + 1. A ratio-approximation would then
    decide whether a Hamiltonian cycle exists."""
    n = len(vertices)
    have = {frozenset((a, b)) for a, b, *_ in roads}
    return {(a, b): (0 if a == b else (1 if frozenset((a, b)) in have else ratio * n + 1)) for a in vertices for b in vertices}


# ---------------------------------------------------------------- greedy set cover

def greedy_set_cover(universe: set, sets: dict) -> list:
    """Repeatedly pick the set covering the most still-uncovered items (Figure 26.6). Within H(n) ~ ln n of the best."""
    uncovered, chosen = set(universe), []
    while uncovered:
        name = max(sorted(sets), key=lambda s: len(sets[s] & uncovered))
        if not sets[name] & uncovered:
            raise ValueError("the sets do not cover the universe")
        chosen.append(name)
        uncovered -= sets[name]
    return chosen


def best_set_cover(universe: set, sets: dict) -> list:
    names = sorted(sets)
    for k in range(len(names) + 1):
        for group in itertools.combinations(names, k):
            if set().union(*[sets[g] for g in group]) >= universe:
                return list(group)


def harmonic(n: int) -> float:
    return sum(1 / i for i in range(1, n + 1))


# The library's suppliers and the titles each can provide (Volume 5, Chapter 17's greedy example, rebuilt).
TITLES = set(range(1, 15))
GRID_SETS = {"row A": set(range(1, 8)), "row B": set(range(8, 15)),
             "block 1": {1, 2, 3, 4, 8, 9, 10, 11}, "block 2": {5, 6, 12, 13}, "block 3": {7, 14}}


# ---------------------------------------------------------------- load balancing

def list_schedule(jobs: list, machines: int) -> tuple[float, list]:
    """Graham's list scheduling: give each job, in the given order, to the least loaded machine."""
    import heapq
    heap = [(0, m) for m in range(machines)]
    loads = [0] * machines
    for j in jobs:
        load, m = heapq.heappop(heap)
        loads[m] = load + j
        heapq.heappush(heap, (loads[m], m))
    return max(loads), loads


def lpt_schedule(jobs: list, machines: int) -> tuple[float, list]:
    """Longest processing time first: sort the jobs largest first, then list-schedule them."""
    return list_schedule(sorted(jobs, reverse=True), machines)


def best_makespan(jobs: list, machines: int) -> float:
    best = None
    for assign in itertools.product(range(machines), repeat=len(jobs)):
        loads = [0] * machines
        for j, m in zip(jobs, assign):
            loads[m] += j
        best = max(loads) if best is None else min(best, max(loads))
    return best


# ---------------------------------------------------------------- k-centre: choosing branch sites

def greedy_k_centre(points: list, k: int) -> tuple[list, float]:
    """Gonzalez's farthest-point rule: start anywhere, then repeatedly open a branch at the point farthest from all
    branches so far. The largest distance from a point to its nearest branch is at most twice the best possible."""
    import math
    centres = [points[0]]
    while len(centres) < min(k, len(points)):
        far = max(points, key=lambda p: min(math.dist(p, c) for c in centres))
        centres.append(far)
    radius = max(min(math.dist(p, c) for c in centres) for p in points)
    return centres, radius


def best_k_centre(points: list, k: int) -> float:
    import math
    return min(max(min(math.dist(p, c) for c in group) for p in points) for group in itertools.combinations(points, k))


HOMES = [(1, 1), (2, 1), (1, 2), (8, 1), (9, 2), (8, 2), (4, 8), (5, 9), (5, 8), (2, 5), (9, 7), (6, 5)]


# ---------------------------------------------------------------- knapsack FPTAS

def knapsack_exact(values: list, weights: list, cap: int) -> int:
    best = [0] * (cap + 1)
    for v, w in zip(values, weights):
        for c in range(cap, w - 1, -1):
            best[c] = max(best[c], best[c - w] + v)
    return best[cap]


def knapsack_by_value(values: list, weights: list, cap: int) -> tuple[int, list]:
    """DP over total value: least weight reaching each value. Returns (best value, chosen indices)."""
    total = sum(values)
    INF = float("inf")
    least = [0] + [INF] * total
    choice = [[] for _ in range(total + 1)]
    for i, (v, w) in enumerate(zip(values, weights)):
        for t in range(total, v - 1, -1):
            if least[t - v] + w < least[t]:
                least[t] = least[t - v] + w
                choice[t] = choice[t - v] + [i]
    best = max(t for t in range(total + 1) if least[t] <= cap)
    return best, choice[best]


def knapsack_fptas(values: list, weights: list, cap: int, eps: float) -> tuple[int, list, int]:
    """Scale values down by K = eps x vmax / n and round down, solve exactly by value, and return the chosen items'
    true value: at least (1 - eps) x the best. Returns (value, chosen, table size)."""
    n = len(values)
    vmax = max((v for v, w in zip(values, weights) if w <= cap), default=0)
    if vmax == 0:
        return 0, [], 0
    K = eps * vmax / n
    scaled = [int(v // K) for v in values]
    _, chosen = knapsack_by_value(scaled, weights, cap)
    return sum(values[i] for i in chosen), chosen, sum(scaled) + 1


SHELF_VALUES = [602, 1012, 845, 377, 1430, 950, 288, 1199, 733, 516]
SHELF_WEIGHTS = [3, 6, 5, 2, 8, 6, 2, 7, 4, 3]


if __name__ == "__main__":
    c = cover_by_matching(ROADS)
    print(c, len(c), smallest_cover(TOWN, ROADS))
    boxes = [7, 6, 5, 4, 4, 3, 2, 2, 2, 1]
    print(first_fit_decreasing(boxes, 10), fewest_bins(boxes, 10))
    r = random.Random(23)
    worst = 0
    for _ in range(200):
        vs = list(range(7))
        es = [e for e in itertools.combinations(vs, 2) if r.random() < 0.35]
        if es:
            worst = max(worst, len(cover_by_matching(es)) / len(smallest_cover(vs, es)))
    print(worst)
    d = travel_times(TOWN, TIMED)
    opt = best_tour(TOWN, d)
    tour, L, w = tree_doubling_tour(TOWN, d)
    ct, cl = christofides(TOWN, d)
    print(opt, mst(TOWN, d), tour, L, w, ct, cl)
    print(greedy_set_cover(TITLES, GRID_SETS), best_set_cover(TITLES, GRID_SETS), round(harmonic(14), 2))
    jobs = [2, 3, 4, 6, 2, 2]
    print(list_schedule(jobs, 3), lpt_schedule(jobs, 3), best_makespan(jobs, 3))
    print(lpt_schedule([3, 3, 2, 2, 2], 2), best_makespan([3, 3, 2, 2, 2], 2), list_schedule([1, 1, 1, 1, 1, 1, 3], 3), best_makespan([1, 1, 1, 1, 1, 1, 3], 3))
    print(greedy_k_centre(HOMES, 3), round(best_k_centre(HOMES, 3), 3))
    print(knapsack_exact(SHELF_VALUES, SHELF_WEIGHTS, 20), knapsack_fptas(SHELF_VALUES, SHELF_WEIGHTS, 20, 0.5), knapsack_fptas(SHELF_VALUES, SHELF_WEIGHTS, 20, 0.1),
          sum(SHELF_VALUES) + 1)
