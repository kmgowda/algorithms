"""Volume 9, Chapter 3 - Bellman-Ford and Negative Edges: Currency Arbitrage.

Run:  python3 ch03_examples.py
"""

from __future__ import annotations

import math
from typing import Hashable

Edge = tuple[Hashable, Hashable, float]


def bellman_ford(vertices: list[Hashable], edges: list[Edge], source: Hashable
                 ) -> tuple[dict[Hashable, float], dict[Hashable, Hashable | None], bool]:
    """Relax EVERY edge, V - 1 rounds. A shortest path uses at most V - 1 edges, and after round k every
    shortest path with <= k edges is correct. If round V still improves something, a negative cycle exists.
    Returns (dist, parent, has_negative_cycle_reachable_from_source). O(V * E)."""
    dist = {v: math.inf for v in vertices}
    parent: dict[Hashable, Hashable | None] = {v: None for v in vertices}
    dist[source] = 0.0
    for _ in range(len(vertices) - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v], parent[v] = dist[u] + w, u
                changed = True
        if not changed:
            break                                   # early stop: already stable
    negative = any(dist[u] + w < dist[v] for u, v, w in edges)
    return dist, parent, negative


def find_negative_cycle(vertices: list[Hashable], edges: list[Edge], eps: float = 0.0) -> list[Hashable] | None:
    """Return one negative cycle (anywhere in the graph), or None.
    Start every vertex at 0 (like a virtual source joined to all), run V rounds, then follow parents back.
    eps ignores improvements smaller than rounding error (needed for floating-point weights like logs)."""
    dist = {v: 0.0 for v in vertices}
    parent: dict[Hashable, Hashable | None] = {v: None for v in vertices}
    last = None
    for _ in range(len(vertices)):
        last = None
        for u, v, w in edges:
            if dist[u] + w < dist[v] - eps:
                dist[v], parent[v] = dist[u] + w, u
                last = v
    if last is None:
        return None
    for _ in range(len(vertices)):                  # step back V times to be sure we're ON the cycle
        last = parent[last]
    cycle, v = [last], parent[last]
    while v != last:
        cycle.append(v)
        v = parent[v]
    return cycle[::-1]


def arbitrage(rates: dict[str, dict[str, float]]) -> list[str] | None:
    """Industry example: exchange rates where some loop of trades returns more money than it started with.
    Multiplying rates > 1 around a loop  <=>  summing -log(rate) < 0: a negative cycle."""
    vertices = list(rates)
    edges = [(a, b, -math.log(r)) for a, nbrs in rates.items() for b, r in nbrs.items()]
    cycle = find_negative_cycle(vertices, edges, eps=1e-12)
    return None if cycle is None else cycle + [cycle[0]]


def cheapest_with_stops(n: int, flights: list[tuple[int, int, int]], src: int, dst: int, k: int) -> int:
    """Practical example (LeetCode 787): cheapest fare using at most k stops = at most k + 1 flights.
    Bellman-Ford limited to k + 1 rounds, copying the distances each round so a round adds only one flight."""
    dist = [math.inf] * n
    dist[src] = 0
    for _ in range(k + 1):
        new = dist[:]
        for a, b, price in flights:
            if dist[a] + price < new[b]:
                new[b] = dist[a] + price
        dist = new
    return -1 if dist[dst] == math.inf else int(dist[dst])


if __name__ == "__main__":
    V = ["A", "B", "C", "D"]
    E = [("A", "B", 4), ("A", "C", 5), ("C", "B", -3), ("B", "D", 2)]
    dist, parent, neg = bellman_ford(V, E, "A")
    print(dist, "negative cycle:", neg)
    rates = {"USD": {"EUR": 0.9, "INR": 83.0}, "EUR": {"INR": 93.0, "USD": 1.11}, "INR": {"USD": 0.0121, "EUR": 0.0108}}
    loop = arbitrage(rates)
    print("arbitrage loop:", loop)
    if loop:
        money = 1.0
        for a, b in zip(loop, loop[1:]):
            money *= rates[a][b]
        print(f"1 unit becomes {money:.4f}")
    print("cheapest with 1 stop:", cheapest_with_stops(3, [(0, 1, 100), (1, 2, 100), (0, 2, 500)], 0, 2, 1))
