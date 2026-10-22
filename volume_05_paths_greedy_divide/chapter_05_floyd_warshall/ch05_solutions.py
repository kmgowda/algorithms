"""Volume 5, Chapter 5 - Thinking Problems: the cheapest round trip (Thinking Problem 2) and the loops in the wrong
order (Thinking Problem 3).

Run:  python3 ch05_solutions.py
"""

from __future__ import annotations

INF = float("inf")


def cheapest_round_trip(n: int, edges: list) -> tuple[float, list | None]:
    """The cheapest cycle of one-way edges (at least one edge) among vertices 0..n-1, assuming no negative cycle.
    Floyd-Warshall with the diagonal started at infinity: dist[i][i] becomes the cheapest way out of i and back.
    Returns (cost, cycle as a list of vertices with the first repeated at the end), or (inf, None)."""
    dist = [[INF] * n for _ in range(n)]
    nxt = [[None] * n for _ in range(n)]
    for a, b, w in edges:
        if w < dist[a][b]:
            dist[a][b], nxt[a][b] = w, b
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    nxt[i][j] = nxt[i][k]
    best = min(range(n), key=lambda i: dist[i][i], default=None)
    if best is None or dist[best][best] == INF:
        return INF, None
    cycle, v = [best], nxt[best][best]
    while v != best:
        cycle.append(v)
        v = nxt[v][best]
    return dist[best][best], cycle + [best]


def floyd_k_innermost(n: int, edges: list) -> list:
    """The WRONG loop order: i, then j, then k innermost, in a single pass."""
    dist = [[0 if i == j else INF for j in range(n)] for i in range(n)]
    for a, b, w in edges:
        dist[a][b] = min(dist[a][b], w)
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist


if __name__ == "__main__":
    import ch05_examples as ex
    idx = {v: i for i, v in enumerate(ex.DEPOTS)}
    print(cheapest_round_trip(5, [(idx[a], idx[b], w) for a, b, w in ex.LEGS]))
    print(floyd_k_innermost(4, [(0, 2, 4), (2, 3, 4), (3, 1, 5)])[0][1])
