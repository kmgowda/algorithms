"""Volume 4, Chapter 31 - Backtracking on Graphs: colouring the map and routes through every place.

Run:  python3 ch31_examples.py
"""

from __future__ import annotations

PLACES = ["Library", "School", "Park", "Market", "Station", "Museum", "Hospital", "Harbour"]
ROADS = [("Library", "School"), ("Library", "Park"), ("School", "Market"), ("Park", "Market"), ("School", "Station"),
         ("Market", "Station"), ("Market", "Museum"), ("Park", "Hospital"), ("Hospital", "Museum"),
         ("Station", "Harbour"), ("Museum", "Harbour"), ("Station", "Museum")]


def neighbours(places: list, roads: list) -> dict:
    adj = {p: set() for p in places}
    for a, b in roads:
        adj[a].add(b)
        adj[b].add(a)
    return adj


def colour(places: list, roads: list, k: int) -> tuple[dict | None, int]:
    """Give each place one of k colours so that no road joins two places of the same colour (Figure 31.1).
    Returns (colouring, nodes visited)."""
    adj, col, nodes = neighbours(places, roads), {}, [0]

    def go(i):
        nodes[0] += 1
        if i == len(places):
            return True
        p = places[i]
        for c in range(k):
            if all(col.get(q) != c for q in adj[p]):
                col[p] = c
                if go(i + 1):
                    return True
                del col[p]
        return False

    return (dict(col) if go(0) else None), nodes[0]


def hamiltonian(places: list, roads: list, start) -> tuple[list, int]:
    """Every route from start visiting each place once, extending only along roads (Figure 31.3)."""
    adj, out, nodes = neighbours(places, roads), [], [0]

    def go(path, seen):
        nodes[0] += 1
        if len(path) == len(places):
            out.append(list(path))
            return
        for q in sorted(adj[path[-1]]):
            if q not in seen:
                path.append(q); seen.add(q)
                go(path, seen)
                path.pop(); seen.remove(q)

    go([start], {start})
    return out, nodes[0]


if __name__ == "__main__":
    for k in (1, 2, 3, 4):
        print(k, colour(PLACES, ROADS, k))
    routes, nodes = hamiltonian(PLACES, ROADS, "Library")
    print(len(routes), nodes, routes[0])
    print(sum(len(hamiltonian(PLACES, ROADS, s)[0]) for s in PLACES))
