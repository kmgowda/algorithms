"""Volume 4, Chapter 25 - Connected Pieces: components, and strongly connected components on one-way streets.

Run:  python3 ch25_examples.py
"""

from __future__ import annotations

from collections import deque

PLACES = ["Library", "School", "Park", "Market", "Station", "Museum", "Hospital", "Harbour"]
ROADS = [("Library", "School"), ("Library", "Park"), ("School", "Market"), ("Park", "Market"), ("School", "Station"),
         ("Market", "Station"), ("Market", "Museum"), ("Park", "Hospital"), ("Hospital", "Museum"),
         ("Station", "Harbour"), ("Museum", "Harbour"), ("Station", "Museum")]
# the storm closes seven roads (Figure 25.1)
CLOSED = {("School", "Market"), ("Park", "Market"), ("School", "Station"), ("Park", "Hospital"), ("Market", "Station"),
          ("Station", "Harbour"), ("Museum", "Harbour")}
# after the storm the council makes some streets one-way (Figure 25.2): (from, to)
ONE_WAY = [("Library", "School"), ("School", "Market"), ("Market", "Park"), ("Park", "Library"), ("Market", "Station"),
           ("Station", "Harbour"), ("Harbour", "Museum"), ("Museum", "Station"), ("Park", "Hospital"),
           ("Hospital", "Museum")]


def adjacency(places=PLACES, roads=ROADS) -> dict:
    adj = {p: [] for p in places}
    for a, b in roads:
        adj[a].append(b)
        adj[b].append(a)
    return adj


def components(adj: dict) -> list[list]:
    """Each piece of an undirected graph: start a BFS from every place not yet reached (Section 25.4)."""
    seen, pieces = set(), []
    for start in adj:
        if start in seen:
            continue
        piece, q = [start], deque([start])
        seen.add(start)
        while q:
            v = q.popleft()
            for w in adj[v]:
                if w not in seen:
                    seen.add(w)
                    piece.append(w)
                    q.append(w)
        pieces.append(piece)
    return pieces


def directed(places=PLACES, arrows=ONE_WAY) -> dict:
    g = {p: [] for p in places}
    for a, b in arrows:
        g[a].append(b)
    return g


def strongly_connected(g: dict) -> list[list]:
    """Kosaraju (Figure 25.3): pass 1 records the finishing order; pass 2 searches the reversed graph."""
    seen, finish = set(), []

    def dfs(v, graph, out):
        seen.add(v)
        for w in graph[v]:
            if w not in seen:
                dfs(w, graph, out)
        out.append(v)                       # v finishes: everything it reaches is done

    for v in g:                             # pass 1, on the one-way streets
        if v not in seen:
            dfs(v, g, finish)
    rev = {v: [] for v in g}
    for v in g:
        for w in g[v]:
            rev[w].append(v)
    seen.clear()
    groups = []
    for v in reversed(finish):              # pass 2, latest finish first, on the reversed streets
        if v not in seen:
            groups.append([])
            dfs(v, rev, groups[-1])
    return groups


def finish_times(g: dict) -> dict:
    """Discovery and finish times of a DFS over the whole directed graph, starting places in list order:
    {place: (discovered, finished)}. Used to illustrate the lemma behind Kosaraju's method (Section 25.6)."""
    clock, times = [0], {}

    def dfs(v):
        clock[0] += 1
        d = clock[0]
        times[v] = (d, None)
        for w in g[v]:
            if w not in times:
                dfs(w)
        clock[0] += 1
        times[v] = (d, clock[0])

    for v in g:
        if v not in times:
            dfs(v)
    return times


def tarjan_scc(g: dict) -> list[list]:
    """Tarjan's one pass (Section 25.6): a place whose low-link equals its own number closes a group."""
    disc, low, on_stack, stack, groups = {}, {}, set(), [], []

    def visit(v):
        disc[v] = low[v] = len(disc) + 1    # discovery numbers 1, 2, 3, ...
        stack.append(v)
        on_stack.add(v)
        for w in g[v]:
            if w not in disc:               # a tree arrow: go deeper, then take the child's low-link
                visit(w)
                low[v] = min(low[v], low[w])
            elif w in on_stack:             # an arrow back into the open group
                low[v] = min(low[v], disc[w])
        if low[v] == disc[v]:               # v is the first place of its group to be reached
            group = []
            while not group or group[-1] != v:
                group.append(stack.pop())
                on_stack.discard(group[-1])
            groups.append(group)

    for v in g:
        if v not in disc:
            visit(v)
    return groups


def tarjan_traced(g: dict, log: list | None = None, final: dict | None = None) -> list[list]:
    """Tarjan's method with a record of its work, for the figures and tests (the same steps as tarjan_scc).
    One DFS gives every place a discovery number disc and a low-link low: the smallest disc
    reachable from its subtree using at most one arrow back to a place still on the stack.
    A place with low = disc is the root of a group: pop the stack down to it. Groups come out sinks first.
    log, if given, receives (place, disc, low, group) as each group root closes its group; final, if given,
    receives {place: (disc, low)} when the search ends."""
    disc, low, on_stack, stack, groups, clock = {}, {}, set(), [], [], [0]

    def visit(v):
        clock[0] += 1
        disc[v] = low[v] = clock[0]
        stack.append(v)
        on_stack.add(v)
        for w in g[v]:
            if w not in disc:                       # a tree arrow: go deeper, then take the child's low-link
                visit(w)
                low[v] = min(low[v], low[w])
            elif w in on_stack:                     # an arrow back into the current, unfinished group
                low[v] = min(low[v], disc[w])
        if low[v] == disc[v]:                       # v is the first place of its group that DFS reached
            group = []
            while True:
                w = stack.pop()
                on_stack.discard(w)
                group.append(w)
                if w == v:
                    break
            groups.append(group)
            if log is not None:
                log.append((v, disc[v], low[v], list(group)))

    for v in g:
        if v not in disc:
            visit(v)
    if final is not None:
        final.update({v: (disc[v], low[v]) for v in disc})
    return groups


def condensation(g: dict, groups: list[list]) -> set:
    """Arrows between groups (by group index): always a DAG."""
    where = {v: i for i, grp in enumerate(groups) for v in grp}
    return {(where[a], where[b]) for a in g for b in g[a] if where[a] != where[b]}


if __name__ == "__main__":
    after = [r for r in ROADS if r not in CLOSED]
    print(components(adjacency(roads=after)))
    print(components(adjacency()))
    print(strongly_connected(directed()))
    print(finish_times(directed()))
    log = []
    print(tarjan_traced(directed(), log), log)
    print(tarjan_scc(directed()))
