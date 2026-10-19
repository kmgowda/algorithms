"""Volume 15, Chapter 3 - Reductions: Turning One Problem Into Another.

A reduction from A to B converts any instance of A into an instance of B with the same answer, quickly.
Then a solver for B solves A - and if A is hard, B must be at least as hard.

Run:  python3 ch03_examples.py
"""

from __future__ import annotations

import itertools

Graph = dict[int, set[int]]
Clause = tuple[int, ...]


def vertex_cover_to_independent_set(graph: Graph, k: int) -> tuple[Graph, int]:
    """S is a vertex cover exactly when the other vertices form an independent set:
    'cover of size <= k?' becomes 'independent set of size >= n - k?' on the SAME graph."""
    return graph, len(graph) - k


def independent_set_to_clique(graph: Graph, k: int) -> tuple[Graph, int]:
    """An independent set in G is a clique in the complement of G (edges flipped)."""
    nodes = list(graph)
    complement = {v: {u for u in nodes if u != v and u not in graph[v]} for v in nodes}
    return complement, k


def coloring_to_sat(graph: Graph, colors: int) -> tuple[list[Clause], int]:
    """k-colouring -> SAT. Variable (v, c) means 'vertex v gets colour c', numbered v * colors + c + 1.
    Clauses: each vertex has a colour, at most one colour, and neighbours differ."""
    nodes = sorted(graph)
    var = {(v, c): i * colors + c + 1 for i, v in enumerate(nodes) for c in range(colors)}
    clauses: list[Clause] = []
    for v in nodes:
        clauses.append(tuple(var[(v, c)] for c in range(colors)))                  # at least one colour
        for c1, c2 in itertools.combinations(range(colors), 2):
            clauses.append((-var[(v, c1)], -var[(v, c2)]))                          # at most one
    for v in nodes:
        for u in graph[v]:
            if v < u:
                for c in range(colors):
                    clauses.append((-var[(v, c)], -var[(u, c)]))                    # neighbours differ
    return clauses, len(var)


def brute_sat(clauses: list[Clause], n_vars: int) -> bool:
    return any(all(any(bits[abs(l) - 1] == (l > 0) for l in cl) for cl in clauses)
               for bits in itertools.product([False, True], repeat=n_vars))


def has_independent_set(graph: Graph, k: int) -> bool:
    return any(all(u not in graph[v] for u, v in itertools.combinations(s, 2))
               for s in itertools.combinations(graph, k)) if k <= len(graph) else False


def has_vertex_cover(graph: Graph, k: int) -> bool:
    edges = [(u, v) for u in graph for v in graph[u] if u < v]
    return any(all(u in s or v in s for u, v in edges) for r in range(min(k, len(graph)) + 1)
               for s in map(set, itertools.combinations(graph, r)))


def has_clique(graph: Graph, k: int) -> bool:
    return any(all(u in graph[v] for u, v in itertools.combinations(s, 2))
               for s in itertools.combinations(graph, k)) if k <= len(graph) else False


def is_colorable(graph: Graph, colors: int) -> bool:
    nodes = sorted(graph)
    return any(all(c[nodes.index(u)] != c[nodes.index(v)] for v in nodes for u in graph[v])
               for c in itertools.product(range(colors), repeat=len(nodes)))


def meeting_rooms_to_coloring(meetings: list[tuple[int, int]]) -> Graph:
    """Industry example: 'can these meetings fit in k rooms?' -> 'is the clash graph k-colourable?'
    (Interval graphs are a special, EASY case - greedy by start time works, V10-C4 - but the reduction shows
    how scheduling problems become graph problems.)"""
    return {i: {j for j, (s2, e2) in enumerate(meetings) if j != i and s1 < e2 and s2 < e1}
            for i, (s1, e1) in enumerate(meetings)}


if __name__ == "__main__":
    square = {0: {1, 3}, 1: {0, 2}, 2: {1, 3}, 3: {0, 2}}
    g, k = vertex_cover_to_independent_set(square, 2)
    print("cover 2:", has_vertex_cover(square, 2), "<-> independent set", k, ":", has_independent_set(g, k))
    comp, k2 = independent_set_to_clique(square, 2)
    print("independent set 2:", has_independent_set(square, 2), "<-> clique in complement:", has_clique(comp, k2))
    triangle = {0: {1, 2}, 1: {0, 2}, 2: {0, 1}}
    for c in (2, 3):
        clauses, n = coloring_to_sat(triangle, c)
        print(f"triangle {c}-colourable: direct {is_colorable(triangle, c)}, via SAT {brute_sat(clauses, n)} "
              f"({len(clauses)} clauses, {n} variables)")
    print(meeting_rooms_to_coloring([(9, 10), (9, 11), (10, 12)]))
