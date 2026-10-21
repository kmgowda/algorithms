"""Volume 3, Chapter 25 - BFS and DFS on the Same Map: orders, trees, frontiers, and what each is good for.

Run:  python3 ch25_examples.py
"""

from __future__ import annotations

from collections import deque

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


def bfs(adj: dict, start) -> dict:
    """Visit order, parents, depth of each place in the tree, and the frontier size after each visit."""
    parent, depth, order, sizes = {start: None}, {start: 0}, [], []
    q = deque([start])
    while q:
        v = q.popleft()
        order.append(v)
        for w in adj[v]:
            if w not in parent:
                parent[w], depth[w] = v, depth[v] + 1
                q.append(w)
        sizes.append(len(q))
    return {"order": order, "parent": parent, "depth": depth, "frontier": sizes}


def dfs(adj: dict, start) -> dict:
    """The same information for depth-first search (explicit stack, same order as the recursive version)."""
    parent, depth, order, sizes = {start: None}, {start: 0}, [start], []
    stack = [(start, iter(adj[start]))]
    while stack:
        v, it = stack[-1]
        for w in it:
            if w not in parent:
                parent[w], depth[w] = v, depth[v] + 1
                order.append(w)
                stack.append((w, iter(adj[w])))
                break
        else:
            stack.pop()
        sizes.append(len(stack))
    return {"order": order, "parent": parent, "depth": depth, "frontier": sizes}


def summary(r: dict) -> dict:
    return {"tree height": max(r["depth"].values()), "largest frontier": max(r["frontier"]) if r["frontier"] else 0}


if __name__ == "__main__":
    adj = adjacency()
    b, d = bfs(adj, "Library"), dfs(adj, "Library")
    print("BFS", b["order"], b["depth"], summary(b))
    print("DFS", d["order"], d["depth"], summary(d))
    star = adjacency(["Hub"] + [f"S{i}" for i in range(100)], [("Hub", f"S{i}") for i in range(100)])
    line = adjacency(list(range(100)), [(i, i + 1) for i in range(99)])
    for name, g, s in (("star", star, "Hub"), ("line", line, 0)):
        print(name, summary(bfs(g, s)), summary(dfs(g, s)))
