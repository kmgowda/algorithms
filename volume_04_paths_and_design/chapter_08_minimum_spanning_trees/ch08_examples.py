"""Volume 4, Chapter 8 - Minimum Spanning Trees: Kruskal and Prim.

Run:  python3 ch08_examples.py
"""

from __future__ import annotations

import heapq

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


if __name__ == "__main__":
    log = []
    k = kruskal(PLACES, ROADS, log)
    for row in log:
        print(row)
    print(total(k), total(ROADS))
    p = prim(PLACES, ROADS, "Library")
    print(p, total(p))
