"""Volume 6, Chapter 7 - model solutions to the Thinking Problems (Section 7.14)."""

from __future__ import annotations

from ch07_examples import neighbours, still_connected


def round_trips(places: list, roads: list, start) -> tuple[list, int]:
    """Every round trip from start through each place once and back along a road (a Hamiltonian cycle), each
    direction once. Prunes when a place is stranded, or when start has no unvisited neighbour left to come home
    through. Returns (trips, nodes visited)."""
    adj, out, nodes = neighbours(places, roads), [], [0]
    if len(places) < 3:
        return [], 0

    def go(path, seen):
        nodes[0] += 1
        if len(path) == len(places):
            if start in adj[path[-1]] and path[1] < path[-1]:
                out.append(path + [start])            # keep one of the two directions
            return
        if not still_connected(adj, path[-1], seen):
            return
        if len(path) > 1 and not any(q not in seen for q in adj[start]):
            return                                    # no road is left on which to come home
        for q in sorted(adj[path[-1]]):
            if q not in seen:
                path.append(q); seen.add(q)
                go(path, seen)
                path.pop(); seen.remove(q)

    go([start], {start})
    return out, nodes[0]


def greedy_colour(places: list, roads: list) -> dict:
    """Thinking Problem 1: colour in list order, each place taking the smallest colour its coloured neighbours
    do not use. Never needs more than (largest degree + 1) colours."""
    adj, col = neighbours(places, roads), {}
    for p in places:
        used = {col[q] for q in adj[p] if q in col}
        col[p] = next(c for c in range(len(places) + 1) if c not in used)
    return col


def one_way_out_bug(places: list, roads: list, start) -> list:
    """Thinking Problem 3's unsound check: back up if some unvisited place has at most one unvisited neighbour."""
    adj, out = neighbours(places, roads), []

    def go(path, seen):
        if len(path) == len(places):
            out.append(list(path))
            return
        if any(sum(q not in seen for q in adj[p]) <= 1 for p in adj if p not in seen):
            return
        for q in sorted(adj[path[-1]]):
            if q not in seen:
                path.append(q); seen.add(q)
                go(path, seen)
                path.pop(); seen.remove(q)

    go([start], {start})
    return out
