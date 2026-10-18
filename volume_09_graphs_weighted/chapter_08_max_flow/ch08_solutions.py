"""Volume 9, Chapter 8 - Solutions to the exercises."""

from __future__ import annotations

from typing import Hashable

from ch08_examples import FlowNetwork


def multi_source_flow(sources: dict[str, float], sinks: dict[str, float], edges: list[tuple[str, str, float]]) -> float:
    """Exercise 1: several factories and shops - add a super-source and super-sink with capacity = supply/demand."""
    net = FlowNetwork()
    for s, supply in sources.items():
        net.add_edge("SUPER_SOURCE", s, supply)
    for t, demand in sinks.items():
        net.add_edge(t, "SUPER_SINK", demand)
    for u, v, c in edges:
        net.add_edge(u, v, c)
    return net.max_flow("SUPER_SOURCE", "SUPER_SINK")[0]


def edge_disjoint_paths(edges: list[tuple[Hashable, Hashable]], s: Hashable, t: Hashable) -> int:
    """Exercise 2: how many routes from s to t share no link? Every link gets capacity 1 (Menger's theorem)."""
    net = FlowNetwork()
    for u, v in edges:
        net.add_edge(u, v, 1)
        net.add_edge(v, u, 1)
    return int(net.max_flow(s, t)[0])


def check_flow(net: FlowNetwork, flow: dict, source: Hashable, sink: Hashable) -> bool:
    """Exercise 3: a valid flow respects capacities and conserves flow at every middle vertex."""
    for u in flow:
        for v, f in flow[u].items():
            if f < 0 or f > net.cap[u][v]:
                return False
    for x in net.cap:
        if x in (source, sink):
            continue
        inflow = sum(flow.get(u, {}).get(x, 0) for u in net.cap)
        outflow = sum(flow.get(x, {}).values())
        if abs(inflow - outflow) > 1e-9:
            return False
    return True


if __name__ == "__main__":
    print(multi_source_flow({"F1": 10, "F2": 5}, {"Shop": 12}, [("F1", "Hub", 8), ("F2", "Hub", 5), ("Hub", "Shop", 20)]))
    print(edge_disjoint_paths([("s", "a"), ("s", "b"), ("a", "t"), ("b", "t"), ("a", "b")], "s", "t"))
