"""Volume 8, Chapter 2 - Graph Vocabulary: Directed, Weighted, Degree, Paths, Cycles.

Run:  python3 ch02_examples.py
"""

from __future__ import annotations

from typing import Hashable

Graph = dict[Hashable, list[Hashable]]
WeightedGraph = dict[Hashable, dict[Hashable, float]]


def is_undirected(graph: Graph) -> bool:
    """Undirected means every edge u -> v has a partner v -> u."""
    return all(u in graph.get(v, []) for u in graph for v in graph[u])


def degree(graph: Graph, v: Hashable) -> int:
    """Undirected: number of edges touching v."""
    return len(graph.get(v, []))


def in_out_degrees(graph: Graph) -> dict[Hashable, tuple[int, int]]:
    """Directed: (edges coming in, edges going out) for each vertex."""
    incoming = {v: 0 for v in graph}
    for u in graph:
        for v in graph[u]:
            incoming[v] = incoming.get(v, 0) + 1
    return {v: (incoming.get(v, 0), len(graph.get(v, []))) for v in set(graph) | set(incoming)}


def is_path(graph: Graph, route: list[Hashable]) -> bool:
    """A path follows edges from each vertex to the next."""
    return all(b in graph.get(a, []) for a, b in zip(route, route[1:]))


def is_simple_path(graph: Graph, route: list[Hashable]) -> bool:
    """A simple path never repeats a vertex."""
    return is_path(graph, route) and len(set(route)) == len(route)


def is_cycle(graph: Graph, route: list[Hashable]) -> bool:
    """A cycle is a path that returns to its start, with no other repeats (and, undirected, at least 3 vertices)."""
    if len(route) < 2 or route[0] != route[-1] or not is_path(graph, route):
        return False
    inner = route[:-1]
    min_len = 3 if is_undirected(graph) else 1
    return len(set(inner)) == len(inner) and len(inner) >= min_len


def path_length(weighted: WeightedGraph, route: list[Hashable]) -> float:
    """Practical example: total distance of a route on a weighted map."""
    return sum(weighted[a][b] for a, b in zip(route, route[1:]))


def handshake_check(graph: Graph) -> bool:
    """The handshake lemma: in an undirected graph, the degrees add up to twice the number of edges."""
    edges = {frozenset((u, v)) for u in graph for v in graph[u]}
    return sum(degree(graph, v) for v in graph) == 2 * len(edges)


def influencers(follows: Graph, top: int) -> list[Hashable]:
    """Industry example: on a 'follows' network, in-degree = followers. Rank accounts by followers."""
    degrees = in_out_degrees(follows)
    return sorted(degrees, key=lambda v: (-degrees[v][0], str(v)))[:top]


if __name__ == "__main__":
    friends = {"Ana": ["Ben", "Cy"], "Ben": ["Ana", "Cy"], "Cy": ["Ana", "Ben", "Dev"], "Dev": ["Cy"]}
    print("undirected:", is_undirected(friends), "| degree of Cy:", degree(friends, "Cy"), "| handshake ok:", handshake_check(friends))
    print("Ana-Ben-Cy-Ana is a cycle:", is_cycle(friends, ["Ana", "Ben", "Cy", "Ana"]),
          "| Ana-Cy-Dev simple path:", is_simple_path(friends, ["Ana", "Cy", "Dev"]))
    follows = {"ana": ["zoo"], "ben": ["zoo", "ana"], "cy": ["zoo"], "zoo": []}
    print("influencers:", influencers(follows, 2), "| degrees:", in_out_degrees(follows)["zoo"])
    roads = {"Pune": {"Mumbai": 150, "Nashik": 210}, "Mumbai": {"Pune": 150, "Surat": 280},
             "Nashik": {"Pune": 210}, "Surat": {"Mumbai": 280}}
    print("Pune-Mumbai-Surat km:", path_length(roads, ["Pune", "Mumbai", "Surat"]))
