"""Volume 4, Chapter 22 - Thinking Problems: model solutions (Section 22.15).

Run:  python3 ch22_solutions.py
"""

from __future__ import annotations


def _limited(adj: dict, path: list, on_path: set, goal, limit: int):
    """Depth-limited DFS that avoids only the places on the current path. Returns (route or None, cut), where
    cut says whether some route was stopped by the limit while it could still have gone on."""
    v = path[-1]
    if v == goal:
        return list(path), False
    if limit == 0:
        return None, any(w not in on_path for w in adj[v])
    cut = False
    for w in adj[v]:
        if w not in on_path:
            path.append(w)
            on_path.add(w)
            found, c = _limited(adj, path, on_path, goal, limit - 1)
            path.pop()
            on_path.discard(w)
            if found:
                return found, False
            cut = cut or c
    return None, cut


def iddfs(adj: dict, start, goal) -> list | None:
    """Thinking Problem 2: iterative deepening. Depth limits 0, 1, 2, ...; the first route found has the fewest
    roads. Memory: the current path only. None when no route was cut off and the goal was not found."""
    limit = 0
    while True:
        found, cut = _limited(adj, [start], {start}, goal, limit)
        if found is not None:
            return found
        if not cut:
            return None
        limit += 1


def count_tree_visits(b: int, d: int) -> tuple[int, int]:
    """Places handled on a tree with b children per place: (one full search to depth d, all rounds 0..d)."""
    layer_sum = lambda k: sum(b ** i for i in range(k + 1))  # noqa: E731
    return layer_sum(d), sum(layer_sum(k) for k in range(d + 1))


def iddfs_shared_visited(adj: dict, start, goal) -> list | None:
    """Thinking Problem 3: the flawed version. Each round keeps one visited set for the whole round, so a place
    first reached by a long route is never tried again by a short one. It can return a route that is too long."""
    for limit in range(len(adj)):
        visited = {start}

        def go(path, left):
            v = path[-1]
            if v == goal:
                return list(path)
            if left == 0:
                return None
            for w in adj[v]:
                if w not in visited:
                    visited.add(w)
                    found = go(path + [w], left - 1)
                    if found:
                        return found
            return None
        found = go([start], limit)
        if found:
            return found
    return None


if __name__ == "__main__":
    import ch22_examples as ex
    print(iddfs(ex.adjacency(), "Library", "Harbour"), count_tree_visits(3, 6))
    g = ex.adjacency(list("SABG"), [("S", "A"), ("A", "B"), ("S", "B"), ("B", "G")])
    print(g, iddfs(g, "S", "G"), iddfs_shared_visited(g, "S", "G"))
