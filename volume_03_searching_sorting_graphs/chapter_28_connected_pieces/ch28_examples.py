"""Volume 3, Chapter 28 - Connected Pieces: components, and strongly connected components on one-way streets.

Run:  python3 ch28_examples.py
"""

from __future__ import annotations

from collections import deque

PLACES = ["Library", "School", "Park", "Market", "Station", "Museum", "Hospital", "Harbour"]
ROADS = [("Library", "School"), ("Library", "Park"), ("School", "Market"), ("Park", "Market"), ("School", "Station"),
         ("Market", "Station"), ("Market", "Museum"), ("Park", "Hospital"), ("Hospital", "Museum"),
         ("Station", "Harbour"), ("Museum", "Harbour"), ("Station", "Museum")]
# the storm closes seven roads (Figure 28.1)
CLOSED = {("School", "Market"), ("Park", "Market"), ("School", "Station"), ("Park", "Hospital"), ("Market", "Station"),
          ("Station", "Harbour"), ("Museum", "Harbour")}
# after the storm the council makes some streets one-way (Figure 28.4): (from, to)
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
    """Each piece of an undirected graph: start a BFS from every place not yet reached (Figure 28.2)."""
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
    """Kosaraju: DFS to get finishing order; then DFS on the reversed graph in reverse finishing order (Figure 28.5).
    Each second-pass tree is one group of places that can all reach each other."""
    seen, finish = set(), []

    def dfs1(v):
        seen.add(v)
        for w in g[v]:
            if w not in seen:
                dfs1(w)
        finish.append(v)

    for v in g:
        if v not in seen:
            dfs1(v)
    rev = {v: [] for v in g}
    for v in g:
        for w in g[v]:
            rev[w].append(v)
    seen.clear()
    groups = []

    def dfs2(v, group):
        seen.add(v)
        group.append(v)
        for w in rev[v]:
            if w not in seen:
                dfs2(w, group)

    for v in reversed(finish):
        if v not in seen:
            group = []
            dfs2(v, group)
            groups.append(group)
    return groups


if __name__ == "__main__":
    after = [r for r in ROADS if r not in CLOSED]
    print(components(adjacency(roads=after)))
    print(components(adjacency()))
    print(strongly_connected(directed()))
