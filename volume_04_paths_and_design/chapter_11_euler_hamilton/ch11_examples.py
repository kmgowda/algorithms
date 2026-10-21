"""Volume 4, Chapter 11 - Euler Tours and Hamiltonian Paths: every road once, or every place once.

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


def euler_kind(places: list, roads: list) -> str:
    """'circuit', 'trail', or 'none' for a connected map (Figure 11.2): count the odd-degree places."""
    odd = sum(1 for d in degrees(places, roads).values() if d % 2)
    return {0: "circuit", 2: "trail"}.get(odd, "none")


def euler_walk(places: list, roads: list) -> list | None:
    """Hierholzer's method (Figure 11.3): walk until stuck, then splice in side loops. None if impossible."""
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


if __name__ == "__main__":
    print(degrees(PLACES, ROADS), euler_kind(PLACES, ROADS))
    w = euler_walk(PLACES, ROADS)
    print(w, len(w))
    hp = hamiltonian_paths(PLACES, ROADS)
    print(len(hp), hp[:2])
