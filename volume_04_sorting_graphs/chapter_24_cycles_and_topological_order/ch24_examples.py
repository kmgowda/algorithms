"""Volume 4, Chapter 24 - Cycles and Topological Order: doing tasks in an order that respects dependencies.

Run:  python3 ch24_examples.py
"""

from __future__ import annotations

from collections import deque

# repairing the old town atlas: (before, after) means "before" must be finished first
TASKS = ["Remove cover", "Clean pages", "Mend tears", "Dry pages", "Resew spine", "Glue spine", "New cover",
         "Label"]
NEEDS = [("Remove cover", "Clean pages"), ("Remove cover", "Resew spine"), ("Clean pages", "Mend tears"),
         ("Clean pages", "Dry pages"), ("Mend tears", "Resew spine"), ("Dry pages", "Resew spine"),
         ("Resew spine", "Glue spine"), ("Glue spine", "New cover"), ("New cover", "Label")]


def graph(tasks=TASKS, needs=NEEDS) -> dict:
    out = {t: [] for t in tasks}
    for a, b in needs:
        out[a].append(b)
    return out


def kahn(g: dict, log: list | None = None) -> list | None:
    """Topological order by repeatedly taking a task with no unfinished prerequisites (Figure 24.2).
    Returns None if some tasks can never start: the graph has a cycle."""
    indeg = {v: 0 for v in g}
    for v in g:
        for w in g[v]:
            indeg[w] += 1
    ready = deque(v for v in g if indeg[v] == 0)
    order = []
    while ready:
        v = ready.popleft()
        order.append(v)
        for w in g[v]:
            indeg[w] -= 1
            if indeg[w] == 0:
                ready.append(w)
        if log is not None:
            log.append((v, list(ready)))
    return order if len(order) == len(g) else None


def dfs_order(g: dict) -> tuple[list | None, list | None]:
    """Topological order as reverse finish order of DFS; also returns a cycle if one is found (grey-grey edge)."""
    WHITE, GREY, BLACK = 0, 1, 2
    colour = {v: WHITE for v in g}
    finished, stack = [], []
    cycle = None

    def visit(v):
        nonlocal cycle
        colour[v] = GREY
        stack.append(v)
        for w in g[v]:
            if colour[w] == GREY and cycle is None:
                cycle = stack[stack.index(w):] + [w]
            elif colour[w] == WHITE:
                visit(w)
        stack.pop()
        colour[v] = BLACK
        finished.append(v)

    for v in g:
        if colour[v] == WHITE:
            visit(v)
    return (None, cycle) if cycle else (finished[::-1], None)


def is_valid_order(g: dict, order: list) -> bool:
    pos = {v: i for i, v in enumerate(order)}
    return len(order) == len(g) and all(pos[a] < pos[b] for a in g for b in g[a])


def closure(g: dict) -> dict:
    """Transitive closure: for every task, the set of tasks that must come after it, by one walk from each task.
    O(V × (V + E)) in all."""
    after = {}
    for start in g:
        seen, stack = set(), [start]
        while stack:
            for w in g[stack.pop()]:
                if w not in seen:
                    seen.add(w)
                    stack.append(w)
        after[start] = seen
    return after


def closure_in_order(g: dict, order: list) -> dict:
    """The same closure on a graph without cycles, using a topological order backwards: a task is followed by its
    direct followers and everything that follows them, already known."""
    after = {}
    for v in reversed(order):
        after[v] = set()
        for w in g[v]:
            after[v] |= {w} | after[w]
    return after


if __name__ == "__main__":
    g = graph()
    log = []
    print(kahn(g, log))
    for row in log:
        print(row)
    print(dfs_order(g))
    bad = graph(needs=NEEDS + [("Label", "Clean pages")])
    print(kahn(bad), dfs_order(bad))
    c = closure(graph())
    print({t: len(v) for t, v in c.items()}, sum(len(v) for v in c.values()))
