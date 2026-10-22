"""Volume 5, Chapter 1 - Thinking Problems: the quickest round that calls at several places (Thinking Problem 2).

Run:  python3 ch01_solutions.py
"""

from __future__ import annotations

import heapq

import ch01_examples as ex


def quickest_visiting_all(adj: dict, start, musts: list, goal) -> tuple[float, list | None, int]:
    """Quickest walk from start to goal that calls at every place in musts, in any order. The states are
    (place, bitmask of musts called at); a single Dijkstra run explores them only as it needs them.
    Returns (minutes, places along the walk, number of states in the whole state graph)."""
    bit = {m: 1 << i for i, m in enumerate(musts)}
    full = (1 << len(musts)) - 1
    first = (start, bit.get(start, 0))
    dist, parent, heap = {first: 0}, {first: None}, [(0, first)]
    while heap:
        d, (v, got) = heapq.heappop(heap)
        if d > dist[(v, got)]:
            continue                                  # an out-of-date entry
        if v == goal and got == full:
            walk, s = [], (v, got)
            while s is not None:
                walk.append(s[0])
                s = parent[s]
            return d, walk[::-1], len(adj) << len(musts)
        for w, m in adj[v].items():
            nxt = (w, got | bit.get(w, 0))
            if d + m < dist.get(nxt, float("inf")):
                dist[nxt], parent[nxt] = d + m, (v, got)
                heapq.heappush(heap, (d + m, nxt))
    return float("inf"), None, len(adj) << len(musts)


if __name__ == "__main__":
    print(quickest_visiting_all(ex.weighted_adjacency(), "Library", ["Market", "School"], "Harbour"))
