"""Volume 5, Chapter 8 - Thinking Problems: which roads are in every, some, or no minimum spanning tree (Thinking
Problem 2), and the split-in-half method that fails (Thinking Problem 3).

Run:  python3 ch08_solutions.py
"""

from __future__ import annotations

from itertools import groupby

import ch08_examples as ex


def _bridges(edges: list) -> set:
    """Ids of the bridges of a multigraph given as (id, u, v) edges: edges on no cycle (Volume 4, Chapter 27).
    Iterative depth-first search with discovery times and low links; parallel edges are never bridges."""
    adj = {}
    for i, u, v in edges:
        adj.setdefault(u, []).append((v, i))
        adj.setdefault(v, []).append((u, i))
    disc, low, out, clock = {}, {}, set(), 0
    for root in adj:
        if root in disc:
            continue
        disc[root] = low[root] = clock
        clock += 1
        stack = [(root, None, iter(adj[root]))]
        while stack:
            v, via, it = stack[-1]
            for w, i in it:
                if i == via:
                    continue
                if w in disc:
                    low[v] = min(low[v], disc[w])
                else:
                    disc[w] = low[w] = clock
                    clock += 1
                    stack.append((w, i, iter(adj[w])))
                    break
            else:
                stack.pop()
                if stack:
                    u = stack[-1][0]
                    low[u] = min(low[u], low[v])
                    if low[v] > disc[u]:
                        out.add(via)
    return out


def classify_roads(places: list, roads: list) -> list:
    """Label every road "every", "some", or "none": in every minimum spanning tree, in some, or in none
    (Thinking Problem 2). Kruskal's groups, one batch of equal weights at a time; within a batch a road joining one
    group is in none, and a road joining two groups is in every tree exactly when it is a bridge of the batch's
    graph of groups. O(E log E). Returns the labels in the order of `roads`."""
    group = {p: p for p in places}

    def find(x):
        while group[x] != x:
            group[x] = group[group[x]]
            x = group[x]
        return x

    label = [""] * len(roads)
    order = sorted(range(len(roads)), key=lambda i: roads[i][2])
    for _, batch in groupby(order, key=lambda i: roads[i][2]):
        batch = list(batch)
        between = []
        for i in batch:
            ga, gb = find(roads[i][0]), find(roads[i][1])
            if ga == gb:
                label[i] = "none"                   # lighter roads already join its ends
            else:
                between.append((i, ga, gb))
        bridges = _bridges(between)
        for i, _, _ in between:
            label[i] = "every" if i in bridges else "some"
        for i in batch:
            ga, gb = find(roads[i][0]), find(roads[i][1])
            if ga != gb:
                group[ga] = gb
    return label


def split_and_join(places: list, roads: list, half: list) -> list:
    """The wrong method of Thinking Problem 3: a minimum tree inside each half, joined by the cheapest road between
    the halves. Returns the tree it builds (which may cost more than the minimum)."""
    inside = set(half)
    other = [p for p in places if p not in inside]
    left = ex.kruskal(list(half), [r for r in roads if r[0] in inside and r[1] in inside])
    right = ex.kruskal(other, [r for r in roads if r[0] not in inside and r[1] not in inside])
    cross = [r for r in roads if (r[0] in inside) != (r[1] in inside)]
    return left + right + ([min(cross, key=lambda r: r[2])] if cross else [])


if __name__ == "__main__":
    print(list(zip(ex.ROADS, classify_roads(ex.PLACES, ex.ROADS))))
    t = split_and_join(ex.PLACES, ex.ROADS, ["Library", "School", "Park", "Station"])
    print(t, ex.total(t))
