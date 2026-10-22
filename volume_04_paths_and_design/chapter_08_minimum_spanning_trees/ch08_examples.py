"""Volume 4, Chapter 8 - Minimum Spanning Trees: Kruskal and Prim.

Run:  python3 ch08_examples.py
"""

from __future__ import annotations

import heapq
import itertools
import random
import time

PLACES = ["Library", "School", "Park", "Market", "Station", "Museum", "Hospital", "Harbour"]
ROADS = [("Library", "School", 4), ("Library", "Park", 3), ("School", "Market", 5), ("Park", "Market", 4),
         ("School", "Station", 9), ("Market", "Station", 3), ("Market", "Museum", 6), ("Park", "Hospital", 5),
         ("Hospital", "Museum", 4), ("Station", "Harbour", 6), ("Museum", "Harbour", 3), ("Station", "Museum", 4)]


def kruskal(places: list, roads: list, log: list | None = None) -> list:
    """Take roads cheapest first, skipping any that would close a loop (Figure 8.2). Uses union-find."""
    parent = {p: p for p in places}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    tree = []
    for a, b, w in sorted(roads, key=lambda r: r[2]):
        ra, rb = find(a), find(b)
        keep = ra != rb
        if keep:
            parent[ra] = rb
            tree.append((a, b, w))
        if log is not None:
            log.append((a, b, w, keep))
    return tree


def prim(places: list, roads: list, start) -> list:
    """Grow one tree from start, always adding the cheapest road leaving it (Figure 8.3)."""
    adj = {p: [] for p in places}
    for a, b, w in roads:
        adj[a].append((w, a, b))
        adj[b].append((w, b, a))
    inside, tree = {start}, []
    heap = list(adj[start])
    heapq.heapify(heap)
    while heap and len(inside) < len(places):
        w, a, b = heapq.heappop(heap)
        if b in inside:
            continue
        inside.add(b)
        tree.append((a, b, w))
        for e in adj[b]:
            if e[2] not in inside:
                heapq.heappush(heap, e)
    return tree


def total(tree: list) -> int:
    return sum(w for _, _, w in tree)


def prim_dense(places: list, roads: list, start) -> list:
    """Prim without a heap (Section 8.5): an array of the cheapest known link to the tree for every outside place,
    scanned for its minimum at each step. O(V^2), the better choice when almost every pair is joined."""
    w = {p: {} for p in places}
    for a, b, c in roads:
        if c < w[a].get(b, float("inf")):
            w[a][b] = w[b][a] = c
    best = {p: (w[start].get(p, float("inf")), start) for p in places if p != start}
    tree = []
    while best:
        v = min(best, key=lambda p: best[p][0])
        cost, via = best.pop(v)
        if cost == float("inf"):
            break                                           # the rest cannot be reached: a forest
        tree.append((via, v, cost))
        for p in best:
            if w[v].get(p, float("inf")) < best[p][0]:
                best[p] = (w[v][p], v)
    return tree


def boruvka(places: list, roads: list, log: list | None = None) -> list:
    """Boruvka (Section 8.5): in each round every group takes its cheapest road out, all at once.
    Ties are broken by the road's position in the list, so no loop can form. O(E log V)."""
    group = {p: p for p in places}

    def find(x):
        while group[x] != x:
            group[x] = group[group[x]]
            x = group[x]
        return x

    order = {r: i for i, r in enumerate(roads)}
    key = lambda r: (r[2], order[r])                       # noqa: E731
    tree = []
    while True:
        cheapest = {}
        for r in roads:
            ga, gb = find(r[0]), find(r[1])
            if ga == gb:
                continue
            for g in (ga, gb):
                if g not in cheapest or key(r) < key(cheapest[g]):
                    cheapest[g] = r
        if not cheapest:
            return tree
        added = []
        for r in sorted(set(cheapest.values()), key=key):
            ga, gb = find(r[0]), find(r[1])
            if ga != gb:
                group[ga] = gb
                tree.append(r)
                added.append(r)
        if log is not None:
            log.append(added)


def minimum_trees(places: list, roads: list) -> list:
    """Every minimum spanning tree, by trying every set of V - 1 roads (tiny maps only)."""
    trees = [list(c) for c in itertools.combinations(roads, len(places) - 1) if len(kruskal(places, list(c))) == len(places) - 1]
    best = min(total(t) for t in trees)
    return [t for t in trees if total(t) == best]


def heaviest_on_loops(places: list, roads: list) -> list:
    """Cycle property (Section 8.5): a road that is the single heaviest on some loop is in no minimum tree.
    Returns the roads found that way: for each road a-b, look for another a-b route using only cheaper roads."""
    out = []
    for a, b, w in roads:
        cheaper = [r for r in roads if r[2] < w]
        reach, stack = {a}, [a]
        while stack:
            v = stack.pop()
            for x, y, _ in cheaper:
                for p, q in ((x, y), (y, x)):
                    if p == v and q not in reach:
                        reach.add(q)
                        stack.append(q)
        if b in reach:
            out.append((a, b, w))
    return out


def clusters(places: list, roads: list, k: int) -> tuple[list, float]:
    """Split the places into k groups with the largest spacing (Section 8.7): run Kruskal and stop when k groups
    remain. Returns (groups, spacing), where spacing is the cheapest road between two different groups."""
    group = {p: p for p in places}

    def find(x):
        while group[x] != x:
            x = group[x]
        return x

    count, spacing = len(places), float("inf")
    for a, b, w in sorted(roads, key=lambda r: r[2]):
        ra, rb = find(a), find(b)
        if ra == rb:
            continue
        if count == k:
            spacing = w
            break
        group[ra] = rb
        count -= 1
    out = {}
    for p in places:
        out.setdefault(find(p), []).append(p)
    return list(out.values()), spacing


def random_map(n: int, m: int, seed: int = 1) -> list:
    """m roads on n places, joined up, with random minutes (complete when m = n(n - 1)/2)."""
    rng = random.Random(seed)
    pairs = {(i - 1, i) for i in range(1, n)}
    if m >= n * (n - 1) // 2:
        pairs = {(i, j) for i in range(n) for j in range(i + 1, n)}
    while len(pairs) < m:
        a, b = sorted(rng.sample(range(n), 2))
        pairs.add((a, b))
    return [(a, b, rng.randint(1, 1000)) for a, b in sorted(pairs)]


def race(n: int, m: int, seed: int = 1) -> dict:
    """Milliseconds for Kruskal, heap Prim, and array Prim on the same random map (Figure 8.6)."""
    places, roads = list(range(n)), random_map(n, m, seed)
    out, totals = {}, set()
    for name, f in (("Kruskal", lambda: kruskal(places, roads)), ("Prim, heap", lambda: prim(places, roads, 0)),
                    ("Prim, array", lambda: prim_dense(places, roads, 0))):
        t = time.perf_counter()
        totals.add(total(f()))
        out[name] = round((time.perf_counter() - t) * 1000, 1)
    assert len(totals) == 1
    return out


if __name__ == "__main__":
    log = []
    k = kruskal(PLACES, ROADS, log)
    for row in log:
        print(row)
    print(total(k), total(ROADS))
    p = prim(PLACES, ROADS, "Library")
    print(p, total(p))
    blog = []
    print(boruvka(PLACES, ROADS, blog), blog)
    print(len(minimum_trees(PLACES, ROADS)), heaviest_on_loops(PLACES, ROADS))
    print(clusters(PLACES, ROADS, 2), clusters(PLACES, ROADS, 3))
    print(race(2000, 6000), race(600, 600 * 599 // 2))
