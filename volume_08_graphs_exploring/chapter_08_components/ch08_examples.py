"""Volume 8, Chapter 8 - Connected Components and Strongly Connected Components.

Run:  python3 ch08_examples.py
"""

from __future__ import annotations

from typing import Hashable

Graph = dict[Hashable, list[Hashable]]


def connected_components(graph: Graph) -> list[list[Hashable]]:
    """Undirected: every vertex not yet labelled starts a new DFS; everything it reaches is one component."""
    seen: set[Hashable] = set()
    components = []
    for start in graph:
        if start in seen:
            continue
        seen.add(start)
        stack, comp = [start], []
        while stack:
            v = stack.pop()
            comp.append(v)
            for w in graph[v]:
                if w not in seen:
                    seen.add(w)
                    stack.append(w)
        components.append(comp)
    return components


def _finish_order(graph: Graph) -> list[Hashable]:
    seen: set[Hashable] = set()
    order: list[Hashable] = []
    for root in graph:
        if root in seen:
            continue
        seen.add(root)
        stack = [(root, iter(graph[root]))]
        while stack:
            v, it = stack[-1]
            w = next(it, None)
            if w is None:
                order.append(v)
                stack.pop()
            elif w not in seen:
                seen.add(w)
                stack.append((w, iter(graph.get(w, []))))
    return order


def kosaraju_scc(graph: Graph) -> list[list[Hashable]]:
    """Directed: a strongly connected component (SCC) is a maximal group where everyone reaches everyone.
    Kosaraju: (1) DFS to get finish order; (2) on the REVERSED graph, DFS in decreasing finish order -
    each search collects exactly one SCC."""
    reverse: Graph = {v: [] for v in graph}
    for u in graph:
        for v in graph[u]:
            reverse.setdefault(v, []).append(u)
    assigned: set[Hashable] = set()
    sccs = []
    for start in reversed(_finish_order(graph)):
        if start in assigned:
            continue
        assigned.add(start)
        stack, comp = [start], []
        while stack:
            v = stack.pop()
            comp.append(v)
            for w in reverse[v]:
                if w not in assigned:
                    assigned.add(w)
                    stack.append(w)
        sccs.append(comp)
    return sccs


def tarjan_scc(graph: Graph) -> list[list[Hashable]]:
    """Tarjan: one DFS. low[v] = smallest discovery index reachable from v's subtree using one back edge
    into the current stack. When low[v] == index[v], v is the root of an SCC - pop it off."""
    index: dict[Hashable, int] = {}
    low: dict[Hashable, int] = {}
    on_stack: set[Hashable] = set()
    stack: list[Hashable] = []
    sccs: list[list[Hashable]] = []
    counter = 0
    for root in graph:
        if root in index:
            continue
        work = [(root, iter(graph[root]))]
        index[root] = low[root] = counter
        counter += 1
        stack.append(root)
        on_stack.add(root)
        while work:
            v, it = work[-1]
            w = next(it, None)
            if w is not None:
                if w not in index:
                    index[w] = low[w] = counter
                    counter += 1
                    stack.append(w)
                    on_stack.add(w)
                    work.append((w, iter(graph.get(w, []))))
                elif w in on_stack:
                    low[v] = min(low[v], index[w])
                continue
            work.pop()
            if work:
                parent = work[-1][0]
                low[parent] = min(low[parent], low[v])
            if low[v] == index[v]:
                comp = []
                while True:
                    x = stack.pop()
                    on_stack.discard(x)
                    comp.append(x)
                    if x == v:
                        break
                sccs.append(comp)
    return sccs


def condensation(graph: Graph) -> tuple[dict[Hashable, int], dict[int, set[int]]]:
    """Shrink every SCC to one vertex: the result is always a DAG (cycles live inside SCCs)."""
    comp_of = {v: i for i, comp in enumerate(kosaraju_scc(graph)) for v in comp}
    dag: dict[int, set[int]] = {i: set() for i in set(comp_of.values())}
    for u in graph:
        for v in graph[u]:
            if comp_of[u] != comp_of[v]:
                dag[comp_of[u]].add(comp_of[v])
    return comp_of, dag


def one_way_neighbourhoods(streets: list[tuple[str, str]]) -> list[list[str]]:
    """Industry example: in a city of one-way streets, which areas can drive to each other and back?"""
    graph: Graph = {}
    for a, b in streets:
        graph.setdefault(a, []).append(b)
        graph.setdefault(b, [])
    return sorted(sorted(c) for c in tarjan_scc(graph))


if __name__ == "__main__":
    friends = {"Ana": ["Ben"], "Ben": ["Ana"], "Cy": ["Dev"], "Dev": ["Cy"], "Eve": []}
    print("friend groups:", connected_components(friends))
    g = {1: [2], 2: [3], 3: [1, 4], 4: [5], 5: [6], 6: [4], 7: [6, 8], 8: []}
    print("Kosaraju:", kosaraju_scc(g))
    print("Tarjan:  ", tarjan_scc(g))
    print("condensation DAG:", condensation(g)[1])
    print(one_way_neighbourhoods([("Old Town", "Market"), ("Market", "Harbour"), ("Harbour", "Old Town"),
                                  ("Harbour", "Airport"), ("Airport", "Hotel"), ("Hotel", "Airport")]))
