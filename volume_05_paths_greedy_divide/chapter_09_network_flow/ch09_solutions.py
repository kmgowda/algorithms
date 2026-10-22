"""Volume 5, Chapter 9 - Thinking Problems: the roads worth widening (Thinking Problem 2) and a minimum cut found
without the backward arrows (Thinking Problem 3).

Run:  python3 ch09_solutions.py
"""

from __future__ import annotations

import ch09_examples as ex


def _reach(room: dict, start, forwards: bool = True) -> set:
    """Places reachable from start along arrows with room > 0 (forwards), or that can reach start (backwards)."""
    seen, stack = {start}, [start]
    while stack:
        v = stack.pop()
        for (a, b), r in room.items():
            x, y = (a, b) if forwards else (b, a)
            if x == v and r > 0 and y not in seen:
                seen.add(y)
                stack.append(y)
    return seen


def upgradable_roads(nodes: list, edges: list, s, t) -> list:
    """The roads whose widening, by any amount, raises the maximum flow (Thinking Problem 2).
    After one maximum flow: road a -> b qualifies exactly when a is reachable from s and t is reachable from b in
    the residual graph. Two searches of the residual graph, O(V + E) after the flow."""
    _, flow = ex.max_flow(nodes, edges, s, t)
    room = ex.residual(edges, flow)
    from_s, to_t = _reach(room, s), _reach(room, t, forwards=False)
    return [(a, b, c) for a, b, c in edges if a in from_s and b in to_t]


def cut_forward_only(nodes: list, edges: list, s, t) -> tuple[set, int]:
    """The buggy cut of Thinking Problem 3: follow only roads that are not full, ignoring the backward arrows.
    Returns (the source side found, its capacity)."""
    _, flow = ex.max_flow(nodes, edges, s, t)
    seen, stack = {s}, [s]
    while stack:
        v = stack.pop()
        for a, b, c in edges:
            if a == v and flow[(a, b)] < c and b not in seen:
                seen.add(b)
                stack.append(b)
    return seen, sum(c for a, b, c in edges if a in seen and b not in seen)


# Thinking Problem 3's network: the forward-only search stops at {s, b, c} and reports a cut of 4, not 2.
TRAP_NODES = ["s", "a", "b", "c", "t"]
TRAP = [("s", "a", 2), ("s", "b", 2), ("a", "c", 2), ("b", "c", 1), ("c", "t", 2)]


if __name__ == "__main__":
    print(upgradable_roads(ex.NODES, ex.PIPES, "Warehouse", "Library"))
    print(cut_forward_only(TRAP_NODES, TRAP, "s", "t"), ex.min_cut(TRAP_NODES, TRAP, "s", "t"))
