"""Volume 3, Chapter 22 - Walking a Graph: the town map, adjacency lists, and the generic explore loop.

Run:  python3 ch22_examples.py
"""

from __future__ import annotations

PLACES = ["Library", "School", "Park", "Market", "Station", "Museum", "Hospital", "Harbour"]
ROADS = [("Library", "School", 4), ("Library", "Park", 3), ("School", "Market", 5), ("Park", "Market", 4),
         ("School", "Station", 9), ("Market", "Station", 3), ("Market", "Museum", 6), ("Park", "Hospital", 5),
         ("Hospital", "Museum", 4), ("Station", "Harbour", 6), ("Museum", "Harbour", 3), ("Station", "Museum", 4)]


def adjacency(places=PLACES, roads=ROADS) -> dict[str, list[str]]:
    """Neighbour lists, in the order the roads are listed (Figure 22.2)."""
    adj = {p: [] for p in places}
    for a, b, _ in roads:
        adj[a].append(b)
        adj[b].append(a)
    return adj


def explore(adj: dict, start, log: list | None = None) -> list:
    """The generic walk (Figure 22.3): keep a frontier of places seen but not yet visited, and a visited set.
    Taking from the end of the frontier makes it a stack (a "stack walk"); taking from the front makes it a queue,
    which is breadth-first search (Chapter 23). The stack walk is NOT depth-first search (Section 22.5)."""
    visited, frontier, order = {start}, [start], []
    while frontier:
        v = frontier.pop()
        order.append(v)
        for w in adj[v]:
            if w not in visited:
                visited.add(w)
                frontier.append(w)
        if log is not None:
            log.append((v, list(frontier)))
    return order


def walk_tree(adj: dict, start, frontier_rule: str = "stack") -> dict:
    """The parent of each place: the place from which it was first seen (the red roads of Figure 22.4)."""
    parent, frontier = {start: None}, [start]
    while frontier:
        v = frontier.pop() if frontier_rule == "stack" else frontier.pop(0)
        for w in adj[v]:
            if w not in parent:
                parent[w] = v
                frontier.append(w)
    return parent


def is_ancestor(parent: dict, a, b) -> bool:
    """True when a lies on the tree path from b back to the start."""
    while b is not None:
        if b == a:
            return True
        b = parent[b]
    return False


def cross_roads(adj: dict, parent: dict) -> list:
    """Roads outside the tree whose ends lie on different branches (neither is an ancestor of the other).
    A depth-first search tree of an undirected graph never has one (Chapter 24)."""
    out = []
    for v in adj:
        for w in adj[v]:
            if v in parent and w in parent and str(v) < str(w) and parent.get(w) != v and parent.get(v) != w \
                    and not is_ancestor(parent, v, w) and not is_ancestor(parent, w, v):
                out.append((v, w))
    return out


def reachable(adj: dict, start) -> set:
    return set(explore(adj, start))


def degree_table(adj: dict) -> dict:
    return {v: len(ws) for v, ws in adj.items()}


if __name__ == "__main__":
    adj = adjacency()
    for v in PLACES:
        print(v, adj[v])
    log = []
    print(explore(adj, "Library", log))
    for row in log:
        print(row)
    print(degree_table(adj), sum(degree_table(adj).values()), len(ROADS))
    t = walk_tree(adj, "Library")
    print(t, cross_roads(adj, t))
