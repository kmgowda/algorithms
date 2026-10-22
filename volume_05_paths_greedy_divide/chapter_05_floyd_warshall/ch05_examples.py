"""Volume 5, Chapter 5 - Every Pair at Once: Floyd-Warshall.

Run:  python3 ch05_examples.py
"""

from __future__ import annotations

import heapq

PLACES = ["Library", "School", "Park", "Market", "Station", "Museum", "Hospital", "Harbour"]
ROADS = [("Library", "School", 4), ("Library", "Park", 3), ("School", "Market", 5), ("Park", "Market", 4),
         ("School", "Station", 9), ("Market", "Station", 3), ("Market", "Museum", 6), ("Park", "Hospital", 5),
         ("Hospital", "Museum", 4), ("Station", "Harbour", 6), ("Museum", "Harbour", 3), ("Station", "Museum", 4)]
INF = float("inf")


def floyd_warshall(n: int, edges: list, directed: bool = False) -> tuple[list, list]:
    """Shortest distances between every pair of vertices 0..n-1 (Figure 5.2).
    Returns (dist, nxt): nxt[i][j] is the first step on a shortest route from i to j."""
    dist = [[0 if i == j else INF for j in range(n)] for i in range(n)]
    nxt = [[j if i == j else None for j in range(n)] for i in range(n)]
    for a, b, w in edges:
        pairs = [(a, b)] if directed else [(a, b), (b, a)]
        for x, y in pairs:
            if w < dist[x][y]:
                dist[x][y], nxt[x][y] = w, y
    for k in range(n):                                # allow k as a stop on the way
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    nxt[i][j] = nxt[i][k]
    return dist, nxt


def path(nxt: list, i: int, j: int) -> list | None:
    if nxt[i][j] is None:
        return None
    out = [i]
    while i != j:
        i = nxt[i][j]
        out.append(i)
    return out


def town_table() -> tuple[list, list]:
    index = {p: i for i, p in enumerate(PLACES)}
    return floyd_warshall(len(PLACES), [(index[a], index[b], w) for a, b, w in ROADS])


def entry_history(i: int, j: int) -> list:
    """The town's i-to-j entry after allowing each place in turn (Figure 5.3)."""
    index = {p: n for n, p in enumerate(PLACES)}
    n = len(PLACES)
    dist = [[0 if a == b else INF for b in range(n)] for a in range(n)]
    for a, b, w in ROADS:
        dist[index[a]][index[b]] = dist[index[b]][index[a]] = w
    history = [dist[i][j]]
    for k in range(n):
        for a in range(n):
            for b in range(n):
                dist[a][b] = min(dist[a][b], dist[a][k] + dist[k][b])
        history.append(dist[i][j])
    return history


def has_negative_cycle(dist: list) -> bool:
    return any(dist[i][i] < 0 for i in range(len(dist)))


def route_by_next_hop(nxt: list, names: list, a, b) -> list | None:
    """RebuildRoute (Section 5.5): walk the next-hop table from a to b, by place names."""
    index = {p: i for i, p in enumerate(names)}
    p = path(nxt, index[a], index[b])
    return None if p is None else [names[i] for i in p]


# The courier's one-way legs from Chapter 3: negative weights, but no negative cycle.
DEPOTS = ["A", "B", "C", "D", "E"]
LEGS = [("A", "B", 6), ("A", "C", 7), ("B", "C", 8), ("B", "D", 5), ("B", "E", -4), ("C", "D", -3), ("C", "E", 9),
        ("D", "B", -2), ("E", "D", 7), ("E", "A", 2)]


def potentials(vertices: list, edges: list) -> dict | None:
    """Bellman-Ford from a new vertex joined to every vertex by a 0-cost leg: h(v) is the cheapest cost of reaching v
    from that new vertex. None if a negative cycle exists."""
    h = {v: 0 for v in vertices}                      # the 0-cost legs from the new vertex, already relaxed
    for _ in range(len(vertices)):                    # V + 1 vertices in all, so V rounds are enough
        changed = False
        for a, b, w in edges:
            if h[a] + w < h[b]:
                h[b] = h[a] + w
                changed = True
        if not changed:
            break
    if any(h[a] + w < h[b] for a, b, w in edges):
        return None                                   # still improving: a negative cycle
    return h


def reweight(edges: list, h: dict) -> list:
    """Each leg a -> b of cost w becomes w + h(a) - h(b), never negative (Section 5.6)."""
    return [(a, b, w + h[a] - h[b]) for a, b, w in edges]


def johnson(vertices: list, edges: list) -> tuple[dict, dict] | None:
    """All-pairs shortest costs with negative legs: one Bellman-Ford for potentials, then Dijkstra from every vertex on
    the reweighted legs, then undo the reweighting. Returns (dist[a][b], h), or None for a negative cycle."""
    h = potentials(vertices, edges)
    if h is None:
        return None
    out = {v: [] for v in vertices}
    for a, b, w in reweight(edges, h):
        out[a].append((b, w))
    dist = {}
    for s in vertices:
        d, heap, done = {s: 0}, [(0, s)], set()
        while heap:
            x, v = heapq.heappop(heap)
            if v in done:
                continue
            done.add(v)
            for w, m in out[v]:
                if x + m < d.get(w, INF):
                    d[w] = x + m
                    heapq.heappush(heap, (d[w], w))
        dist[s] = {t: (d[t] - h[s] + h[t] if t in d else INF) for t in vertices}
    return dist, h


if __name__ == "__main__":
    dist, nxt = town_table()
    for p, row in zip(PLACES, dist):
        print(f"{p:9s}", row)
    print([PLACES[i] for i in path(nxt, 0, 7)])
    print(sum(sum(r) for r in dist) / 2, max(max(r) for r in dist))
