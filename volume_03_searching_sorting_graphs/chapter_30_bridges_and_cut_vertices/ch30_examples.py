"""Volume 3, Chapter 30 - Weak Links: Bridges and Cut Vertices, found with one DFS and low-links.

Run:  python3 ch30_examples.py
"""

from __future__ import annotations

PLACES = ["Library", "School", "Park", "Market", "Station", "Museum", "Hospital", "Harbour"]
ROADS = [("Library", "School"), ("Library", "Park"), ("School", "Market"), ("Park", "Market"), ("School", "Station"),
         ("Market", "Station"), ("Market", "Museum"), ("Park", "Hospital"), ("Hospital", "Museum"),
         ("Station", "Harbour"), ("Museum", "Harbour"), ("Station", "Museum")]
# the district beyond the town: one lane to the Lighthouse, one track to the Farm
OUTER = ["Lighthouse", "Farm"]
OUTER_ROADS = [("Harbour", "Lighthouse"), ("Hospital", "Farm")]


def adjacency(places, roads) -> dict:
    adj = {p: [] for p in places}
    for a, b in roads:
        adj[a].append(b)
        adj[b].append(a)
    return adj


def weak_links(adj: dict) -> dict:
    """One DFS (Figure 30.3). low[v] = the earliest discovery time reachable from v's subtree using at most one
    back road. Tree road (u, v) is a bridge if low[v] > disc[u]; u is a cut vertex if some child v has
    low[v] >= disc[u] (the root: if it has two or more children)."""
    disc, low, parent = {}, {}, {}
    bridges, cuts = [], set()
    time = [0]

    def visit(u):
        time[0] += 1
        disc[u] = low[u] = time[0]
        children = 0
        for v in adj[u]:
            if v not in disc:
                parent[v] = u
                children += 1
                visit(v)
                low[u] = min(low[u], low[v])
                if low[v] > disc[u]:
                    bridges.append((u, v))
                if parent.get(u) is not None and low[v] >= disc[u]:
                    cuts.add(u)
            elif v != parent.get(u):
                low[u] = min(low[u], disc[v])
        if parent.get(u) is None and children >= 2:
            cuts.add(u)

    for s in adj:
        if s not in disc:
            parent[s] = None
            visit(s)
    return {"disc": disc, "low": low, "bridges": bridges, "cuts": sorted(cuts, key=lambda p: disc[p])}


def brute_force(adj: dict) -> dict:
    """Check by removal: a road is a bridge if removing it disconnects its ends; a place is a cut vertex if
    removing it increases the number of pieces."""
    def pieces(a, skip_place=None, skip_road=None):
        seen, n = set(), 0
        for s in a:
            if s == skip_place or s in seen:
                continue
            n += 1
            stack = [s]
            seen.add(s)
            while stack:
                v = stack.pop()
                for w in a[v]:
                    if w == skip_place or {v, w} == skip_road or w in seen:
                        continue
                    seen.add(w)
                    stack.append(w)
        return n
    base = pieces(adj)
    roads = {frozenset((u, v)) for u in adj for v in adj[u] if u != v}
    return {"bridges": {r for r in roads if pieces(adj, skip_road=set(r)) > base},
            "cuts": {p for p in adj if pieces(adj, skip_place=p) > base - (1 if not adj[p] else 0)}}


if __name__ == "__main__":
    town = adjacency(PLACES, ROADS)
    r = weak_links(town)
    print(r["bridges"], r["cuts"])
    big = adjacency(PLACES + OUTER, ROADS + OUTER_ROADS)
    r = weak_links(big)
    print(r["bridges"], r["cuts"])
    print({p: (r["disc"][p], r["low"][p]) for p in sorted(r["disc"], key=r["disc"].get)})
    print(brute_force(big))
