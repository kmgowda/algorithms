"""Volume 6, Chapter 22 - DP on Graphs: counting quickest routes, and routes with a limited number of roads.

Run:  python3 ch22_examples.py
"""

from __future__ import annotations

import heapq

PLACES = ["Library", "School", "Park", "Market", "Station", "Museum", "Hospital", "Harbour"]
ROADS = [("Library", "School", 4), ("Library", "Park", 3), ("School", "Market", 5), ("Park", "Market", 4),
         ("School", "Station", 9), ("Market", "Station", 3), ("Market", "Museum", 6), ("Park", "Hospital", 5),
         ("Hospital", "Museum", 4), ("Station", "Harbour", 6), ("Museum", "Harbour", 3), ("Station", "Museum", 4)]
# Roadworks day: the School-Station road reopens as a 6-minute road and the Museum-Harbour road slows to 4 minutes.
ROADWORKS = [(a, b, {("School", "Station"): 6, ("Museum", "Harbour"): 4}.get((a, b), w)) for a, b, w in ROADS]
# Volume 5, Chapter 3's courier legs, with bonuses.
DEPOTS = ["A", "B", "C", "D", "E"]
LEGS = [("A", "B", 6), ("A", "C", 7), ("B", "C", 8), ("B", "D", 5), ("B", "E", -4), ("C", "D", -3), ("C", "E", 9),
        ("D", "B", -2), ("E", "D", 7), ("E", "A", 2)]


def adjacency(places=PLACES, roads=ROADS) -> dict:
    adj = {p: {} for p in places}
    for a, b, w in roads:
        adj[a][b] = adj[b][a] = w
    return adj


def count_quickest(adj: dict, start) -> tuple[dict, dict]:
    """Dijkstra, plus ways[v] = number of quickest routes to v. Places are settled in time order,
    so every quickest route into v comes from an already-settled place."""
    dist, ways, done = {start: 0}, {start: 1}, set()
    heap = [(0, start)]
    while heap:
        d, v = heapq.heappop(heap)
        if v in done:
            continue
        done.add(v)
        for w, m in adj[v].items():
            if d + m < dist.get(w, float("inf")):
                dist[w], ways[w] = d + m, ways[v]
                heapq.heappush(heap, (d + m, w))
            elif d + m == dist[w] and w not in done:
                ways[w] += ways[v]                     # another quickest route arrives (never into a settled place)
    return dist, ways


def at_most_k(vertices: list, edges: list, start, k: int) -> list:
    """best[i][v] = cheapest cost to v using at most i legs (Figure 22.2): Bellman-Ford as a table."""
    inf = float("inf")
    rows = [{v: (0 if v == start else inf) for v in vertices}]
    for _ in range(k):
        prev, cur = rows[-1], dict(rows[-1])
        for a, b, w in edges:
            if prev[a] + w < cur[b]:
                cur[b] = prev[a] + w
        rows.append(cur)
    return rows


def count_paths_dag(order: list, edges: list, start) -> dict:
    """Routes from start to every vertex of a DAG, in topological order."""
    ways = {v: 0 for v in order}
    ways[start] = 1
    for v in order:
        for a, b in edges:
            if a == v:
                ways[b] += ways[v]
    return ways


if __name__ == "__main__":
    dist, ways = count_quickest(adjacency(), "Library")
    print(dist, ways)
    print(count_quickest(adjacency(PLACES, ROADWORKS), "Library"))
    for i, row in enumerate(at_most_k(DEPOTS, LEGS, "A", 4)):
        print(i, row)
    course = ["Basics", "Lists", "Trees", "Graphs", "Search", "Project"]
    pre = [("Basics", "Lists"), ("Basics", "Trees"), ("Lists", "Graphs"), ("Trees", "Graphs"), ("Lists", "Search"),
           ("Graphs", "Project"), ("Search", "Project"), ("Trees", "Project")]
    print(count_paths_dag(course, pre, "Basics"))
