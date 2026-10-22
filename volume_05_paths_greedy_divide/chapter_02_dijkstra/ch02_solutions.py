"""Volume 5, Chapter 2 - Thinking Problems: the widest route (Thinking Problem 2) and the meet-in-the-middle
stopping rule (Thinking Problem 3).

Run:  python3 ch02_solutions.py
"""

from __future__ import annotations

import heapq


def widest_routes(adj: dict, start) -> tuple[dict, dict]:
    """For every reachable place, the largest load that can travel from start (the best route's smallest road
    limit) and its parent. Dijkstra with max instead of +: settle the place with the largest width first."""
    width, parent = {start: float("inf")}, {start: None}
    heap, settled = [(-width[start], start)], set()
    while heap:
        negw, v = heapq.heappop(heap)
        if v in settled:
            continue
        settled.add(v)
        for w, limit in adj[v].items():
            through = min(-negw, limit)
            if through > width.get(w, float("-inf")):
                width[w] = through
                parent[w] = v
                heapq.heappush(heap, (-through, w))
    return width, parent


def meet_first_settled_twice(adj: dict, s, t):
    """The WRONG two-ended rule: alternate one settle from s and one from t, and stop at the first place settled by
    both searches, answering its two times added. Returns (answer, meeting place)."""
    if s == t:
        return 0, s
    dist, heap, settled = [{s: 0}, {t: 0}], [[(0, s)], [(0, t)]], [set(), set()]
    side = 0
    while heap[0] or heap[1]:
        if not heap[side]:
            side = 1 - side
        d, v = heapq.heappop(heap[side])
        if v in settled[side]:
            continue
        settled[side].add(v)
        if v in settled[1 - side]:
            return dist[0][v] + dist[1][v], v
        for w, m in adj[v].items():
            if d + m < dist[side].get(w, float("inf")):
                dist[side][w] = d + m
                heapq.heappush(heap[side], (d + m, w))
        side = 1 - side
    return None, None


def meet_in_middle(adj: dict, s, t):
    """The corrected two-ended search for two-way roads: remember the best route seen across any road joining the
    two searches, and stop once the two smallest heap keys add up to at least that best."""
    if s == t:
        return 0
    dist, heap, settled = [{s: 0}, {t: 0}], [[(0, s)], [(0, t)]], [set(), set()]
    best, side = float("inf"), 0
    while heap[0] and heap[1]:
        if heap[0][0][0] + heap[1][0][0] >= best:
            break
        d, v = heapq.heappop(heap[side])
        if v not in settled[side]:
            settled[side].add(v)
            for w, m in adj[v].items():
                if w in dist[1 - side]:
                    best = min(best, d + m + dist[1 - side][w])
                if d + m < dist[side].get(w, float("inf")):
                    dist[side][w] = d + m
                    heapq.heappush(heap[side], (d + m, w))
        side = 1 - side
    return None if best == float("inf") else best


if __name__ == "__main__":
    tri = {"S": {"A": 3, "T": 5}, "A": {"S": 3, "T": 3}, "T": {"S": 5, "A": 3}}
    print(meet_first_settled_twice(tri, "S", "T"), meet_in_middle(tri, "S", "T"))
