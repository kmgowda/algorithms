"""Volume 5, Chapter 7 - Thinking Problems.

Problem 1: the bidirectional stopping rule (top of both heaps >= mu) never stops early (checked on random maps).
Problem 2: the nearest of several libraries from every place, with one Dijkstra started from all of them.
Problem 3: the naive rule 'stop at the first place settled by both sides' can answer wrongly; a smallest counterexample.
"""

from __future__ import annotations

import heapq

from ch07_examples import bidirectional, dij, random_map


def multi_source(adj: dict, sources: list) -> tuple[dict, dict]:
    """Every place's distance to its nearest source, and which source that is: Dijkstra with all sources at 0."""
    dist, near = {s: 0 for s in sources}, {s: s for s in sources}
    heap, done = [(0, s, s) for s in sources], set()
    heapq.heapify(heap)
    while heap:
        d, v, src = heapq.heappop(heap)
        if v in done:
            continue
        done.add(v)
        for w, m in adj[v].items():
            if d + m < dist.get(w, float("inf")):
                dist[w], near[w] = d + m, src
                heapq.heappush(heap, (d + m, w, src))
    return dist, near


def naive_counterexample() -> tuple[float, float]:
    """(naive answer, correct answer) on a small map where they differ."""
    adj = {"S": {"M": 5, "T": 9}, "M": {"S": 5, "T": 6}, "T": {"S": 9, "M": 6}}      # a triangle
    return bidirectional(adj, "S", "T", naive=True)[0], bidirectional(adj, "S", "T")[0]


if __name__ == "__main__":
    adj = dij.weighted_adjacency()
    print(multi_source(adj, ["Library", "Harbour"]))
    print(naive_counterexample())
