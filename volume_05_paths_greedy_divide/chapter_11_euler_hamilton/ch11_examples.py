"""Volume 5, Chapter 11 - Euler Tours and Hamiltonian Paths: every road once, or every place once.

Run:  python3 ch11_examples.py
"""

from __future__ import annotations

import itertools

PLACES = ["Library", "School", "Park", "Market", "Station", "Museum", "Hospital", "Harbour"]
ROADS = [("Library", "School"), ("Library", "Park"), ("School", "Market"), ("Park", "Market"), ("School", "Station"),
         ("Market", "Station"), ("Market", "Museum"), ("Park", "Hospital"), ("Hospital", "Museum"),
         ("Station", "Harbour"), ("Museum", "Harbour"), ("Station", "Museum")]


def degrees(places: list, roads: list) -> dict:
    deg = {p: 0 for p in places}
    for a, b in roads:
        deg[a] += 1
        deg[b] += 1
    return deg


def one_piece(roads: list) -> bool:
    """True when every road can be reached from every other: all the places that have a road are connected.
    (Places with no road at all do not matter.)"""
    if not roads:
        return True
    adj: dict = {}
    for a, b in roads:
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)
    start = roads[0][0]
    seen, stack = {start}, [start]
    while stack:
        for w in adj[stack.pop()]:
            if w not in seen:
                seen.add(w)
                stack.append(w)
    return len(seen) == len(adj)


def euler_kind(places: list, roads: list) -> str:
    """'circuit', 'trail', or 'none' (Figure 11.2): the roads must form one piece, and the number of odd-degree places
    must be 0 (a circuit) or 2 (a trail)."""
    if not one_piece(roads):
        return "none"
    odd = sum(1 for d in degrees(places, roads).values() if d % 2)
    return {0: "circuit", 2: "trail"}.get(odd, "none")


def euler_walk(places: list, roads: list) -> list | None:
    """Hierholzer's method, stack form (Section 11.4): walk until stuck, then splice in side loops. None if impossible."""
    kind = euler_kind(places, roads)
    if kind == "none" or not roads:
        return None if kind == "none" else []
    adj = {p: [] for p in places}
    for i, (a, b) in enumerate(roads):
        adj[a].append((b, i))
        adj[b].append((a, i))
    deg = degrees(places, roads)
    start = next((p for p in places if deg[p] % 2), next(p for p in places if deg[p]))
    used, stack, walk = set(), [start], []
    while stack:
        v = stack[-1]
        while adj[v] and adj[v][-1][1] in used:
            adj[v].pop()
        if adj[v]:
            w, i = adj[v].pop()
            used.add(i)
            stack.append(w)
        else:
            walk.append(stack.pop())
    return walk[::-1] if len(used) == len(roads) else None


def hamiltonian_paths(places: list, roads: list) -> list:
    """Every route visiting each place exactly once, by trying every order (n! of them)."""
    edges = {frozenset(r) for r in roads}
    out = []
    for order in itertools.permutations(places):
        if order[0] < order[-1] and all(frozenset(p) in edges for p in zip(order, order[1:])):
            out.append(list(order))
    return out


MINUTES = {("Library", "School"): 4, ("Library", "Park"): 3, ("School", "Market"): 5, ("Park", "Market"): 4,
           ("School", "Station"): 9, ("Market", "Station"): 3, ("Market", "Museum"): 6, ("Park", "Hospital"): 5,
           ("Hospital", "Museum"): 4, ("Station", "Harbour"): 6, ("Museum", "Harbour"): 3, ("Station", "Museum"): 4}


def postman_extra(roads: list) -> tuple[int, list]:
    """Section 11.7: the cheapest way to pair up the odd places, repeating quickest routes between pairs."""
    places = sorted({p for r in roads for p in r})
    inf = float("inf")
    d = {(a, b): 0 if a == b else inf for a in places for b in places}
    for a, b in roads:
        d[(a, b)] = d[(b, a)] = MINUTES[(a, b)]
    for k in places:
        for i in places:
            for j in places:
                d[(i, j)] = min(d[(i, j)], d[(i, k)] + d[(k, j)])
    odd = [p for p, n in degrees(places, roads).items() if n % 2]

    def pairings(rest):
        if not rest:
            yield []
            return
        a = rest[0]
        for i in range(1, len(rest)):
            for more in pairings(rest[1:i] + rest[i + 1:]):
                yield [(a, rest[i])] + more

    return min((sum(d[p] for p in pr), pr) for pr in pairings(odd))


def hierholzer_pieces(places: list, roads: list) -> tuple[list, list]:
    """Hierholzer's method by splicing (Figure 11.3): walk from the start until stuck, trying each place's roads in
    list order; then, while some place on the
    walk still has unused roads, walk a side loop from it and splice the loop in at that place.
    Returns (the pieces walked, in order, the final walk)."""
    if euler_kind(places, roads) == "none":
        return [], []
    if not roads:
        return [], []
    adj = {p: [] for p in places}
    for i, (a, b) in reversed(list(enumerate(roads))):  # so each place tries its roads in list order
        adj[a].append((b, i))
        adj[b].append((a, i))
    used: set = set()

    def walk_from(v):
        piece = [v]
        while True:
            while adj[v] and adj[v][-1][1] in used:
                adj[v].pop()
            if not adj[v]:
                return piece
            w, i = adj[v].pop()
            used.add(i)
            piece.append(w)
            v = w

    deg = degrees(places, roads)
    start = next((p for p in places if deg[p] % 2), next(p for p in places if deg[p]))
    walk = walk_from(start)
    pieces = [list(walk)]
    while len(used) < len(roads):
        k = next(k for k, v in enumerate(walk) if any(i not in used for _, i in adj[v]))
        loop = walk_from(walk[k])
        pieces.append(loop)
        walk = walk[:k] + loop + walk[k + 1:]
    return pieces, walk


def euler_walk_directed(places: list, streets: list) -> list | None:
    """Every one-way street exactly once (Section 11.4): possible when the streets form one piece and every place has
    as many streets in as out (a circuit), or one place has one extra out (the start) and one has one extra in (the
    end). Hierholzer's method, following streets forwards only. None if impossible."""
    out_deg = {p: 0 for p in places}
    in_deg = {p: 0 for p in places}
    for a, b in streets:
        out_deg[a] += 1
        in_deg[b] += 1
    starts = [p for p in places if out_deg[p] - in_deg[p] == 1]
    ends = [p for p in places if in_deg[p] - out_deg[p] == 1]
    balanced = all(abs(out_deg[p] - in_deg[p]) <= 1 for p in places)
    if not streets:
        return []
    if not balanced or not one_piece(streets) or (len(starts), len(ends)) not in ((0, 0), (1, 1)):
        return None
    adj = {p: [] for p in places}
    for a, b in reversed(streets):
        adj[a].append(b)
    stack, walk = [starts[0] if starts else streets[0][0]], []
    while stack:
        v = stack[-1]
        if adj[v]:
            stack.append(adj[v].pop())
        else:
            walk.append(stack.pop())
    return walk[::-1] if len(walk) == len(streets) + 1 else None

if __name__ == "__main__":
    print(degrees(PLACES, ROADS), euler_kind(PLACES, ROADS))
    w = euler_walk(PLACES, ROADS)
    print(w, len(w))
    hp = hamiltonian_paths(PLACES, ROADS)
    print(len(hp), hp[:2])
