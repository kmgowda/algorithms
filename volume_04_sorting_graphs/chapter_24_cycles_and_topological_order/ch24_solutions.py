"""Volume 4, Chapter 24 - Thinking Problems: model solutions that are algorithms.

Run:  python3 ch24_solutions.py
"""

from __future__ import annotations

from ch24_examples import NEEDS, graph, kahn


def order_or_cycle(g: dict) -> tuple[str, list]:
    """Thinking Problem 2: Kahn's method that, when it gets stuck, also names a cycle. O(V + E).
    Returns ("order", topological order) or ("cycle", [v1, v2, ..., v1]) along the arrows."""
    log = []
    order = kahn(g, log)                        # Section 24.4, with its record of finished tasks
    if order is not None:
        return "order", order
    done = {v for v, _ in log}
    pred = {}                                   # one arrow into each leftover task from another leftover task
    for v in g:
        if v not in done:
            for w in g[v]:
                if w not in done:
                    pred[w] = v
    v, seen = next(v for v in g if v not in done), {}
    walk = []
    while v not in seen:                        # walk backwards until a task repeats
        seen[v] = len(walk)
        walk.append(v)
        v = pred[v]
    loop = walk[seen[v]:]                       # backwards along the arrows: v, pred(v), pred(pred(v)), ...
    loop.reverse()
    return "cycle", loop + [loop[0]]


def discovery_order(g: dict) -> list:
    """Thinking Problem 3: the flawed method 'list tasks in the order DFS discovers them'."""
    seen, order = set(), []

    def visit(v):
        seen.add(v)
        order.append(v)
        for w in g[v]:
            if w not in seen:
                visit(w)

    for v in g:
        if v not in seen:
            visit(v)
    return order


if __name__ == "__main__":
    print(order_or_cycle(graph()))
    print(order_or_cycle(graph(needs=NEEDS + [("Label", "Clean pages")])))
    print(discovery_order(graph()))
