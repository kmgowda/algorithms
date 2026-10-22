"""Volume 7, Chapter 26 - Thinking Problem 2: the smallest vertex cover of a tree (or forest) in linear time.

Run:  python3 ch26_solutions.py
"""

from __future__ import annotations


def tree_cover(edges: list) -> set:
    """Smallest cover of a forest: visit children before parents; when the road to a parent is still bare,
    post the warden at the parent. The roads that trigger a warden share no ends, so no cover is smaller."""
    adj = {}
    for a, b in edges:
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)
    parent, order = {}, []
    for root in adj:
        if root in parent:
            continue
        parent[root] = None
        stack = [root]
        while stack:
            v = stack.pop()
            order.append(v)
            for u in adj[v]:
                if u not in parent:
                    parent[u] = v
                    stack.append(u)
    cover = set()
    for v in reversed(order):                      # every child comes before its parent
        p = parent[v]
        if p is not None and v not in cover and p not in cover:
            cover.add(p)
    return cover


if __name__ == "__main__":
    town_tree = [("Library", "Park"), ("Library", "School"), ("Park", "Market"), ("Market", "Station"),
                 ("Station", "Museum"), ("Museum", "Harbour"), ("Museum", "Hospital")]
    print(sorted(tree_cover(town_tree)))
