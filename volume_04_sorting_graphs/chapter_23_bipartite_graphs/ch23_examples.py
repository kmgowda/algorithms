"""Volume 4, Chapter 23 - Two Colours: Bipartite Graphs.

Run:  python3 ch23_examples.py
"""

from __future__ import annotations

from collections import deque

PLACES = ["Library", "School", "Park", "Market", "Station", "Museum", "Hospital", "Harbour"]
ROADS = [("Library", "School"), ("Library", "Park"), ("School", "Market"), ("Park", "Market"), ("School", "Station"),
         ("Market", "Station"), ("Market", "Museum"), ("Park", "Hospital"), ("Hospital", "Museum"),
         ("Station", "Harbour"), ("Museum", "Harbour"), ("Station", "Museum")]
# the reading club's debate: members who have argued before must be on opposite teams
MEMBERS = ["Ana", "Ben", "Cai", "Dev", "Eva", "Fay", "Gus"]
QUARRELS = [("Ana", "Ben"), ("Ana", "Dev"), ("Ben", "Cai"), ("Cai", "Dev"), ("Dev", "Eva"), ("Eva", "Fay"),
            ("Fay", "Gus")]


def adjacency(places, roads) -> dict:
    adj = {p: [] for p in places}
    for a, b in roads:
        adj[a].append(b)
        adj[b].append(a)
    return adj


def two_colour(adj: dict) -> tuple[dict | None, list | None]:
    """BFS colouring (Figure 23.2): neighbours get the opposite colour. Returns (colours, None) if the graph is
    bipartite, else (None, odd cycle) built from the two BFS tree paths that meet at a same-coloured edge."""
    colour, parent = {}, {}
    for s in adj:
        if s in colour:
            continue
        colour[s], parent[s] = 0, None
        q = deque([s])
        while q:
            v = q.popleft()
            for w in adj[v]:
                if w not in colour:
                    colour[w], parent[w] = 1 - colour[v], v
                    q.append(w)
                elif colour[w] == colour[v]:
                    return None, odd_cycle(parent, v, w)
    return colour, None


def odd_cycle(parent: dict, a, b) -> list:
    """Climb from a and b to their nearest common ancestor; the two paths plus edge a-b form an odd cycle."""
    pa, x = [], a
    while x is not None:
        pa.append(x)
        x = parent[x]
    pb, x = [], b
    while x not in pa:
        pb.append(x)
        x = parent[x]
    top = pa.index(x)
    return pa[:top + 1] + pb[::-1] + [a]


def teams(colour: dict) -> tuple[list, list]:
    return [v for v in colour if colour[v] == 0], [v for v in colour if colour[v] == 1]


if __name__ == "__main__":
    c, cyc = two_colour(adjacency(MEMBERS, QUARRELS))
    print(teams(c), cyc)
    c2, cyc2 = two_colour(adjacency(MEMBERS, QUARRELS + [("Ben", "Dev")]))
    print(c2, cyc2)
    print(two_colour(adjacency(PLACES, ROADS)))
