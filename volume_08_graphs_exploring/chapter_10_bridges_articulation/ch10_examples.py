"""Volume 8, Chapter 10 - Bridges, Articulation Points, and Network Reliability.

Run:  python3 ch10_examples.py
"""

from __future__ import annotations

from typing import Hashable

Graph = dict[Hashable, list[Hashable]]


def low_links(graph: Graph) -> tuple[dict, dict, dict]:
    """One iterative DFS over an undirected graph.
    disc[v] = discovery time; low[v] = earliest discovery time reachable from v's DFS subtree
    using at most one non-tree (back) edge; parent[v] = DFS tree parent."""
    disc: dict[Hashable, int] = {}
    low: dict[Hashable, int] = {}
    parent: dict[Hashable, Hashable | None] = {}
    clock = 0
    for root in graph:
        if root in disc:
            continue
        parent[root] = None
        disc[root] = low[root] = clock
        clock += 1
        stack = [(root, iter(graph[root]))]
        while stack:
            v, it = stack[-1]
            w = next(it, None)
            if w is None:
                stack.pop()
                p = parent[v]
                if p is not None:
                    low[p] = min(low[p], low[v])        # a child's escape route is also the parent's
            elif w not in disc:
                parent[w] = v
                disc[w] = low[w] = clock
                clock += 1
                stack.append((w, iter(graph[w])))
            elif w != parent[v]:
                low[v] = min(low[v], disc[w])            # back edge to an ancestor
    return disc, low, parent


def bridges(graph: Graph) -> list[tuple[Hashable, Hashable]]:
    """Tree edge p - v is a bridge when v's subtree can't reach p or above without it: low[v] > disc[p]."""
    disc, low, parent = low_links(graph)
    return sorted((p, v) for v, p in parent.items() if p is not None and low[v] > disc[p])


def articulation_points(graph: Graph) -> list[Hashable]:
    """A vertex whose removal disconnects the graph.
    Non-root p: some child v has low[v] >= disc[p]. Root: it has two or more DFS children."""
    disc, low, parent = low_links(graph)
    children: dict[Hashable, int] = {}
    points = set()
    for v, p in parent.items():
        if p is None:
            continue
        children[p] = children.get(p, 0) + 1
        if parent[p] is not None and low[v] >= disc[p]:
            points.add(p)
    points |= {v for v, p in parent.items() if p is None and children.get(v, 0) >= 2}
    return sorted(points, key=str)


def critical_cables(n: int, cables: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Industry example (LeetCode 1192): data-centre cables whose failure would split the network."""
    graph: Graph = {v: [] for v in range(n)}
    for a, b in cables:
        graph[a].append(b)
        graph[b].append(a)
    return [tuple(sorted(e)) for e in bridges(graph)]    # type: ignore[misc]


def single_points_of_failure(roads: list[tuple[str, str]]) -> list[str]:
    """Industry example: towns whose closure (a flood, roadworks) cuts the road network into pieces."""
    graph: Graph = {}
    for a, b in roads:
        graph.setdefault(a, []).append(b)
        graph.setdefault(b, []).append(a)
    return articulation_points(graph)                    # type: ignore[return-value]


if __name__ == "__main__":
    print("critical cables:", critical_cables(4, [(0, 1), (1, 2), (2, 0), (1, 3)]))
    roads = [("Pune", "Lonavala"), ("Lonavala", "Mumbai"), ("Mumbai", "Thane"), ("Thane", "Lonavala"),
             ("Pune", "Satara"), ("Satara", "Kolhapur")]
    print("single points of failure:", single_points_of_failure(roads))
    g = {v: [] for v in "ABCDEFG"}
    for a, b in ["AB", "BC", "CA", "CD", "DE", "EF", "FD", "EG"]:
        g[a].append(b)
        g[b].append(a)
    print("bridges:", bridges(g), "| articulation points:", articulation_points(g))
