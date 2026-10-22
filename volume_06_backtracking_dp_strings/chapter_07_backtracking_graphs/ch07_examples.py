"""Volume 6, Chapter 7 - Backtracking on Graphs: colouring the map and routes through every place.

Run:  python3 ch07_examples.py
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
    """Give each place one of k colours so that no road joins two places of the same colour (Figure 7.1).
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
    """Every route from start visiting each place once, extending only along roads (Figure 7.3)."""
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


def still_connected(adj: dict, end, seen: set) -> bool:
    """Can the route's end still reach every unvisited place through unvisited places? (Section 7.5)"""
    left = [p for p in adj if p not in seen]
    if not left:
        return True
    reach, stack = set(), [end]
    while stack:
        v = stack.pop()
        for q in adj[v]:
            if q not in seen and q not in reach:
                reach.add(q)
                stack.append(q)
    return len(reach) == len(left)


def hamiltonian_pruned(places: list, roads: list, start, first_only: bool = False) -> tuple[list, int]:
    """Routes from start through every place, backing up as soon as some unvisited place is cut off."""
    adj, out, nodes = neighbours(places, roads), [], [0]

    def go(path, seen):
        nodes[0] += 1
        if len(path) == len(places):
            out.append(list(path))
            return first_only
        if not still_connected(adj, path[-1], seen):
            return False                              # a stranded place: no route can finish
        for q in sorted(adj[path[-1]]):
            if q not in seen:
                path.append(q); seen.add(q)
                if go(path, seen):
                    return True
                path.pop(); seen.remove(q)
        return False

    go([start], {start})
    return out, nodes[0]


def grid_map(rows: int, cols: int) -> tuple[list, list]:
    """The reading room's tables in a rows x cols grid, each joined to its neighbours left, right, up, and down."""
    places = [(r, c) for r in range(rows) for c in range(cols)]
    roads = [((r, c), (r, c + 1)) for r in range(rows) for c in range(cols - 1)]
    roads += [((r, c), (r + 1, c)) for r in range(rows - 1) for c in range(cols)]
    return places, roads


def hamiltonian_first(places: list, roads: list, start) -> tuple[list | None, int]:
    """Plain search stopping at the first route, for comparison with hamiltonian_pruned(first_only=True)."""
    adj, nodes = neighbours(places, roads), [0]

    def go(path, seen):
        nodes[0] += 1
        if len(path) == len(places):
            return list(path)
        for q in sorted(adj[path[-1]]):
            if q not in seen:
                path.append(q); seen.add(q)
                found = go(path, seen)
                if found:
                    return found
                path.pop(); seen.remove(q)
        return None

    return go([start], {start}), nodes[0]


def colour_ordered(places: list, roads: list, k: int, order: str) -> tuple[dict | None, int]:
    """k-colouring by backtracking with a choice of which place to colour next (Section 7.4):
    'list' takes the places in the order given; 'degree' takes the most-connected place first;
    'dsatur' takes, each time, the uncoloured place whose neighbours already use the most different colours
    (ties to the most-connected). Returns (colouring, nodes)."""
    adj, col, nodes = neighbours(places, roads), {}, [0]
    by_degree = sorted(places, key=lambda p: -len(adj[p]))

    def pick():
        left = [p for p in (places if order == "list" else by_degree) if p not in col]
        if order != "dsatur":
            return left[0]
        return max(left, key=lambda p: (len({col[q] for q in adj[p] if q in col}), len(adj[p])))

    def go():
        nodes[0] += 1
        if len(col) == len(places):
            return True
        p = pick()
        for c in range(k):
            if all(col.get(q) != c for q in adj[p]):
                col[p] = c
                if go():
                    return True
                del col[p]
        return False

    return (dict(col) if go() else None), nodes[0]


def fewest_colours(places: list, roads: list, order: str) -> tuple[int, int]:
    """Try k = 1, 2, 3, ... until a colouring exists. Returns (chromatic number, total nodes over every k)."""
    total = 0
    for k in range(1 if places else 0, len(places) + 1):
        col, n = colour_ordered(places, roads, k, order)
        total += n
        if col is not None:
            return k, total
    return 0, total


def random_graph(n: int, p: float, seed: int) -> tuple[list, list]:
    import random
    r = random.Random(seed)
    places = list(range(n))
    return places, [(a, b) for a in places for b in places if a < b and r.random() < p]


if __name__ == "__main__":
    for k in (1, 2, 3, 4):
        print(k, colour(PLACES, ROADS, k))
    routes, nodes = hamiltonian(PLACES, ROADS, "Library")
    print(len(routes), nodes, routes[0])
    print(sum(len(hamiltonian(PLACES, ROADS, s)[0]) for s in PLACES))
