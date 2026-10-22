"""Volume 4, Chapter 20 - Thinking Problems: model solutions (Section 20.14).

Run:  python3 ch20_solutions.py
"""

from __future__ import annotations

from collections import deque

from ch20_examples import bfs


def on_shortest_routes(adj: dict, a, b) -> set:
    """Thinking Problem 2: every place lying on at least one fewest-roads route from a to b (two-way roads).
    Two BFS runs: w qualifies exactly when dist_a[w] + dist_b[w] = dist_a[b]. O(V + E)."""
    da, _ = bfs(adj, a)
    if b not in da:
        return set()
    db, _ = bfs(adj, b)
    return {w for w in da if w in db and da[w] + db[w] == da[b]}


def meet_in_middle_wrong(adj: dict, s, t):
    """Thinking Problem 3: the flawed bidirectional BFS. It takes one place at a time from each side in turn and
    stops at the first place seen by both, reporting the sum of its two distances. Can be too long."""
    if s == t:
        return 0
    da, db, qa, qb = {s: 0}, {t: 0}, deque([s]), deque([t])
    while qa and qb:
        for q, d, other in ((qa, da, db), (qb, db, da)):
            v = q.popleft()
            for w in adj[v]:
                if w not in d:
                    d[w] = d[v] + 1
                    q.append(w)
                    if w in other:
                        return d[w] + other[w]
            if not q:
                return None
    return None


def meet_in_middle(adj: dict, s, t):
    """The repaired version: expand one whole layer at a time, alternating sides; when a layer touches the other
    side's seen places, return the smallest total over all the roads of that layer that touch it."""
    if s == t:
        return 0
    da, db, la, lb = {s: 0}, {t: 0}, [s], [t]
    while la and lb:
        best, nxt = None, []
        for v in la:
            for w in adj[v]:
                if w in db and (best is None or da[v] + 1 + db[w] < best):
                    best = da[v] + 1 + db[w]
                if w not in da:
                    da[w] = da[v] + 1
                    nxt.append(w)
        if best is not None:
            return best
        da, db, la, lb = db, da, lb, nxt
    return None


if __name__ == "__main__":
    import ch20_examples as ex
    print(sorted(on_shortest_routes(ex.adjacency(), "Library", "Museum")))
    g = ex.adjacency(list("SABCDT"), [("S", "A"), ("S", "C"), ("A", "B"), ("B", "D"), ("C", "D"), ("D", "T")])
    print(meet_in_middle_wrong(g, "S", "T"), meet_in_middle(g, "S", "T"), bfs(g, "S")[0]["T"])
