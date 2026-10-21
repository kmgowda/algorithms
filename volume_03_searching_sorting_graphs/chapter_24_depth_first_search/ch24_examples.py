"""Volume 3, Chapter 24 - Depth-First Search: go as deep as you can, then back up.

Run:  python3 ch24_examples.py
"""

from __future__ import annotations

PLACES = ["Library", "School", "Park", "Market", "Station", "Museum", "Hospital", "Harbour"]
ROADS = [("Library", "School"), ("Library", "Park"), ("School", "Market"), ("Park", "Market"), ("School", "Station"),
         ("Market", "Station"), ("Market", "Museum"), ("Park", "Hospital"), ("Hospital", "Museum"),
         ("Station", "Harbour"), ("Museum", "Harbour"), ("Station", "Museum")]


def adjacency(places=PLACES, roads=ROADS) -> dict:
    adj = {p: [] for p in places}
    for a, b in roads:
        adj[a].append(b)
        adj[b].append(a)
    return adj


def dfs(adj: dict, start) -> dict:
    """Recursive DFS (Figure 24.2): discovery and finish times, parents, and the kind of every road met."""
    time = [0]
    disc, fin, parent, edges = {}, {}, {start: None}, []

    def visit(v):
        time[0] += 1
        disc[v] = time[0]
        for w in adj[v]:
            if w not in disc:
                parent[w] = v
                edges.append((v, w, "tree"))
                visit(w)
            elif w != parent[v] and w not in fin:
                edges.append((v, w, "back"))       # leads to an ancestor still being explored: a cycle
        time[0] += 1
        fin[v] = time[0]

    visit(start)
    return {"disc": disc, "fin": fin, "parent": parent, "edges": edges,
            "order": sorted(disc, key=disc.get)}


def dfs_iterative(adj: dict, start) -> list:
    """The same visiting order with an explicit stack (no recursion limit)."""
    order, seen, stack = [], set(), [(start, iter(adj[start]))]
    seen.add(start)
    order.append(start)
    while stack:
        v, it = stack[-1]
        for w in it:
            if w not in seen:
                seen.add(w)
                order.append(w)
                stack.append((w, iter(adj[w])))
                break
        else:
            stack.pop()
    return order


def find_path(adj: dict, a, b) -> list | None:
    """Some route from a to b (not necessarily the shortest), by DFS parents."""
    r = dfs(adj, a)
    if b not in r["parent"]:
        return None
    path = []
    while b is not None:
        path.append(b)
        b = r["parent"][b]
    return path[::-1]


if __name__ == "__main__":
    r = dfs(adjacency(), "Library")
    print(r["order"])
    print({v: (r["disc"][v], r["fin"][v]) for v in r["order"]})
    print([e for e in r["edges"] if e[2] == "back"])
    print(dfs_iterative(adjacency(), "Library"), find_path(adjacency(), "Library", "Harbour"))
