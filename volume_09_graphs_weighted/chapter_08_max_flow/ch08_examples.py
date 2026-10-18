"""Volume 9, Chapter 8 - Network Flow: Ford-Fulkerson and Edmonds-Karp.

Run:  python3 ch08_examples.py
"""

from __future__ import annotations

from collections import deque
from typing import Hashable


class FlowNetwork:
    """Directed edges with capacities. Residual capacity: cap[u][v] - flow[u][v]; pushing flow u->v also
    creates 'undo' capacity v->u (the flow can be sent back later if a better plan appears)."""

    def __init__(self) -> None:
        self.cap: dict[Hashable, dict[Hashable, float]] = {}

    def add_edge(self, u: Hashable, v: Hashable, capacity: float) -> None:
        self.cap.setdefault(u, {}).setdefault(v, 0)
        self.cap.setdefault(v, {}).setdefault(u, 0)              # reverse edge, capacity 0 initially
        self.cap[u][v] += capacity

    def max_flow(self, source: Hashable, sink: Hashable) -> tuple[float, dict[Hashable, dict[Hashable, float]]]:
        """Edmonds-Karp: repeatedly find the SHORTEST augmenting path (BFS) in the residual graph and push
        as much as its narrowest edge allows. O(V E^2). Returns (value, flow on each edge)."""
        residual = {u: dict(nbrs) for u, nbrs in self.cap.items()}
        total = 0.0
        while True:
            parent: dict[Hashable, Hashable | None] = {source: None}
            queue = deque([source])
            while queue and sink not in parent:
                u = queue.popleft()
                for v, c in residual[u].items():
                    if c > 0 and v not in parent:
                        parent[v] = u
                        queue.append(v)
            if sink not in parent:
                break                                            # no augmenting path left: flow is maximum
            bottleneck, v = float("inf"), sink
            while parent[v] is not None:
                u = parent[v]
                bottleneck = min(bottleneck, residual[u][v])      # type: ignore[index]
                v = u                                            # type: ignore[assignment]
            v = sink
            while parent[v] is not None:
                u = parent[v]
                residual[u][v] -= bottleneck                      # type: ignore[index]
                residual[v][u] += bottleneck                      # type: ignore[index]
                v = u                                            # type: ignore[assignment]
            total += bottleneck
        self._residual = residual
        flow = {u: {v: max(0, self.cap[u][v] - residual[u][v]) for v in self.cap[u] if self.cap[u][v] > 0}
                for u in self.cap}                               # net flow; two-way pairs keep only the positive side
        return total, flow

    def min_cut(self, source: Hashable) -> tuple[set[Hashable], list[tuple[Hashable, Hashable]]]:
        """After max_flow: vertices still reachable from the source in the residual graph form one side;
        the full edges leaving that side are a minimum cut (their capacities sum to the max flow)."""
        side, queue = {source}, deque([source])
        while queue:
            u = queue.popleft()
            for v, c in self._residual[u].items():
                if c > 0 and v not in side:
                    side.add(v)
                    queue.append(v)
        cut = [(u, v) for u in side for v in self.cap[u] if v not in side and self.cap[u][v] > 0]
        return side, sorted(cut, key=str)


def evacuation_capacity(roads: list[tuple[str, str, int]], town: str, shelter: str) -> tuple[float, list]:
    """Industry example: people per hour that can move from a town to a shelter, and the roads that limit it."""
    net = FlowNetwork()
    for a, b, c in roads:
        net.add_edge(a, b, c)
    value, _ = net.max_flow(town, shelter)
    return value, net.min_cut(town)[1]


if __name__ == "__main__":
    net = FlowNetwork()
    for u, v, c in [("S", "A", 10), ("S", "B", 5), ("A", "B", 15), ("A", "T", 5), ("B", "T", 10)]:
        net.add_edge(u, v, c)
    value, flow = net.max_flow("S", "T")
    print("max flow:", value, "| flow:", {u: f for u, f in flow.items() if f})
    print("min cut:", net.min_cut("S"))
    roads = [("Town", "Bridge", 700), ("Town", "Hill road", 300), ("Bridge", "Shelter", 500),
             ("Hill road", "Shelter", 400), ("Bridge", "Hill road", 200)]
    print("evacuation:", evacuation_capacity(roads, "Town", "Shelter"))
