"""Volume 4, Chapter 25 - Thinking Problems: model solutions that are algorithms.

Run:  python3 ch25_solutions.py
"""

from __future__ import annotations

from collections import deque

from ch25_examples import directed, finish_times


def reach(g: dict, start) -> set:
    """Every place reachable from start along the arrows (BFS)."""
    seen, q = {start}, deque([start])
    while q:
        for w in g[q.popleft()]:
            if w not in seen:
                seen.add(w)
                q.append(w)
    return seen


def depots(g: dict) -> list:
    """Thinking Problem 2: every place from which all places can be reached, in O(V + E).
    The place that finishes last in a DFS of the whole graph is the only candidate worth testing
    (it lies in a group no arrow enters); if it reaches everything, the depots are exactly the
    places that can reach it."""
    if not g:
        return []
    times = finish_times(g)                         # pass 1 of Kosaraju (Section 25.6)
    last = max(g, key=lambda v: times[v][1])
    if len(reach(g, last)) < len(g):
        return []
    rev = {v: [] for v in g}
    for v in g:
        for w in g[v]:
            rev[w].append(v)
    back = reach(rev, last)
    return [v for v in g if v in back]


def tarjan_any_visited(g: dict) -> list[list]:
    """Thinking Problem 3: the flawed Tarjan that lowers low[v] through ANY discovered place,
    including places whose group is already finished and popped."""
    disc, low, stack, groups = {}, {}, [], []

    def visit(v):
        disc[v] = low[v] = len(disc) + 1
        stack.append(v)
        for w in g[v]:
            if w not in disc:
                visit(w)
                low[v] = min(low[v], low[w])
            else:                                   # the bug: no "is w still on the stack?" test
                low[v] = min(low[v], disc[w])
        if low[v] == disc[v]:
            group = []
            while not group or group[-1] != v:
                group.append(stack.pop())
            groups.append(group)

    for v in g:
        if v not in disc:
            visit(v)
    return groups


if __name__ == "__main__":
    print(depots(directed()))
    print(tarjan_any_visited({"R": ["X", "Y"], "X": [], "Y": ["X"]}))
