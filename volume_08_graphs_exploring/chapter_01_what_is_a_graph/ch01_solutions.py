"""Volume 8, Chapter 1 - Solutions to the exercises."""

from __future__ import annotations

from typing import Hashable

from ch01_examples import Graph, can_reach, make_undirected


def count_roads(graph: Graph) -> int:
    """Exercise 1: each two-way road is listed twice, once per end."""
    return sum(len(v) for v in graph.values()) // 2


def most_connected(graph: Graph) -> Hashable:
    """Exercise 2: the city with the most roads."""
    return max(graph, key=lambda v: (len(graph[v]), str(v)))


def mutual_friends(friends: Graph, a: Hashable, b: Hashable) -> set:
    """Exercise 3: friends shared by a and b."""
    return set(friends.get(a, [])) & set(friends.get(b, []))


def unreachable_from(graph: Graph, start: Hashable) -> list:
    """Exercise 4: every city you can't drive to from start."""
    return sorted(v for v in graph if not can_reach(graph, start, v))


if __name__ == "__main__":
    g = make_undirected([("Pune", "Mumbai"), ("Mumbai", "Surat"), ("Pune", "Nashik"), ("Goa", "Panaji")])
    print(count_roads(g), most_connected(g), mutual_friends(make_undirected([("a", "c"), ("b", "c")]), "a", "b"), unreachable_from(g, "Pune"))
