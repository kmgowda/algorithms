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
    """The same visiting order with an explicit stack (Section 24.4): each stack entry remembers how far along its
    place's neighbour list the search has got, so the stack is exactly the current path (no recursion limit)."""
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


# Section 24.6, Figure 24.4: one-way streets of the old quarter, with neighbours in this order
QUARTER = {"Library": ["School", "Park", "Market"], "School": ["Market"], "Market": ["Library"],
           "Park": ["Market", "Hospital"], "Hospital": []}


def classify_directed(adj: dict, starts=None) -> dict:
    """DFS over a directed graph, restarting from every undiscovered place in list order (Figure 24.4).
    Each arrow v -> w is a tree, back, forward, or cross arrow, decided by w's state when the arrow is followed:
    undiscovered (tree); discovered but unfinished, an ancestor (back); finished and discovered after v, a
    descendant (forward); finished and discovered before v, another branch (cross)."""
    time = [0]
    disc, fin, kinds = {}, {}, []

    def visit(v):
        time[0] += 1
        disc[v] = time[0]
        for w in adj[v]:
            if w not in disc:
                kinds.append((v, w, "tree"))
                visit(w)
            elif w not in fin:
                kinds.append((v, w, "back"))
            elif disc[w] > disc[v]:
                kinds.append((v, w, "forward"))
            else:
                kinds.append((v, w, "cross"))
        time[0] += 1
        fin[v] = time[0]

    for s in (starts if starts is not None else adj):
        if s not in disc:
            visit(s)
    return {"disc": disc, "fin": fin, "edges": kinds}


def white_path_descendants(adj: dict, u, discovered: set) -> set:
    """The white-path theorem: the places that will become u's descendants are exactly those reachable from u
    along places all still undiscovered at the moment u is discovered (u itself included)."""
    seen, stack = {u}, [u]
    while stack:
        v = stack.pop()
        for w in adj[v]:
            if w not in seen and w not in discovered:
                seen.add(w)
                stack.append(w)
    return seen


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
    c = classify_directed(QUARTER)
    print(c)
    print(white_path_descendants(QUARTER, "Park", {"Library", "School", "Market"}))
