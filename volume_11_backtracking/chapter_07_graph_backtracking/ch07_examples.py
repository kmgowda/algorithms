"""Volume 11, Chapter 7 - Graph Backtracking: Graph Coloring, Hamiltonian Cycles.

Run:  python3 ch07_examples.py
"""

from __future__ import annotations

from typing import Hashable

Graph = dict[Hashable, list[Hashable]]


def m_coloring(graph: Graph, m: int) -> dict[Hashable, int] | None:
    """Colour vertices with colours 0..m-1 so neighbours differ, or None. Backtracking, most-constrained-first:
    colour next the uncoloured vertex whose neighbours already use the most different colours."""
    color: dict[Hashable, int] = {}

    def saturation(v: Hashable) -> tuple[int, int]:
        return len({color[w] for w in graph[v] if w in color}), len(graph[v])

    def go() -> bool:
        if len(color) == len(graph):
            return True
        v = max((u for u in graph if u not in color), key=saturation)
        used = {color[w] for w in graph[v] if w in color}
        for c in range(m):
            if c in used:
                continue
            color[v] = c
            if go():
                return True
            del color[v]
        return False

    return dict(color) if go() else None


def chromatic_number(graph: Graph) -> int:
    """The fewest colours that work: try m = 1, 2, 3, ... (exact, exponential in the worst case)."""
    if not graph:
        return 0
    m = 1
    while m_coloring(graph, m) is None:
        m += 1
    return m


def hamiltonian_cycle(graph: Graph) -> list[Hashable] | None:
    """A cycle visiting every vertex exactly once. Fix the start (all rotations are the same cycle - symmetry),
    extend the path to unvisited neighbours, and prune if some unvisited vertex has no way in or out."""
    vertices = list(graph)
    if not vertices:
        return None
    start = vertices[0]
    path, on_path = [start], {start}

    def dead_end() -> bool:
        for v in graph:
            if v not in on_path:
                usable = [w for w in graph[v] if w not in on_path or w in (path[-1], start)]
                if len(usable) < 2 and len(graph) > 2:
                    return True
        return False

    def go() -> bool:
        if len(path) == len(vertices):
            return start in graph[path[-1]]
        if dead_end():
            return False
        for w in graph[path[-1]]:
            if w not in on_path:
                path.append(w)
                on_path.add(w)
                if go():
                    return True
                path.pop()
                on_path.remove(w)
        return False

    return path + [start] if go() else None


def knights_tour(n: int) -> list[tuple[int, int]] | None:
    """Practical example: a knight visiting every square once. Warnsdorff's ordering - move to the square with
    the fewest onward moves first - usually finds a tour with almost no backtracking."""
    jumps = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
    seen = {(0, 0)}
    path = [(0, 0)]

    def moves(r: int, c: int) -> list[tuple[int, int]]:
        return [(r + dr, c + dc) for dr, dc in jumps
                if 0 <= r + dr < n and 0 <= c + dc < n and (r + dr, c + dc) not in seen]

    def go() -> bool:
        if len(path) == n * n:
            return True
        for nxt in sorted(moves(*path[-1]), key=lambda sq: len(moves(*sq))):
            seen.add(nxt)
            path.append(nxt)
            if go():
                return True
            path.pop()
            seen.remove(nxt)
        return False

    return list(path) if go() else None


def register_allocation(interference: Graph, registers: int) -> dict[Hashable, int] | None:
    """Industry example: give each variable a CPU register; variables alive at the same time interfere.
    An exact colouring with a fixed number of colours (V8-C9 used the greedy version)."""
    return m_coloring(interference, registers)


def undirected(edges: list[tuple[str, str]]) -> Graph:
    g: Graph = {}
    for a, b in edges:
        g.setdefault(a, []).append(b)
        g.setdefault(b, []).append(a)
    return g


if __name__ == "__main__":
    states = undirected([("WA", "NT"), ("WA", "SA"), ("NT", "SA"), ("NT", "Q"), ("SA", "Q"), ("SA", "NSW"),
                         ("SA", "V"), ("Q", "NSW"), ("NSW", "V")])
    print("3-colouring of Australia:", m_coloring(states, 3), "| chromatic number:", chromatic_number(states))
    cube = undirected([("a", "b"), ("b", "c"), ("c", "d"), ("d", "a"), ("e", "f"), ("f", "g"), ("g", "h"),
                       ("h", "e"), ("a", "e"), ("b", "f"), ("c", "g"), ("d", "h")])
    print("Hamiltonian cycle on a cube:", hamiltonian_cycle(cube))
    print("star has one?", hamiltonian_cycle(undirected([("hub", "x"), ("hub", "y"), ("hub", "z")])))
    tour = knights_tour(6)
    print("knight's tour on 6x6:", len(tour), "squares, starts", tour[:4])
    regs = undirected([("x", "y"), ("y", "z"), ("x", "z"), ("z", "w")])
    print("registers:", register_allocation(regs, 3), register_allocation(regs, 2))
