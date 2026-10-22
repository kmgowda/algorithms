"""Volume 4, Chapter 24 - Thinking Problems: model solutions.

Run:  python3 ch24_solutions.py
"""

from __future__ import annotations

from ch24_examples import OUTER, OUTER_ROADS, PLACES, ROADS, adjacency, weak_links


def one_way_plan(adj: dict) -> list[tuple] | None:
    """Thinking Problem 1 (Robbins): make every road one-way so that, inside each piece, every place can still
    reach every other; possible exactly when there is no bridge. Tree roads point down the DFS tree, every other
    road points up, from the later-discovered end to the earlier. Returns the directed roads (self-loops left
    out), or None if there is a bridge."""
    if weak_links(adj)["bridges"]:
        return None
    disc, out = {}, []

    def visit(u, parent):
        disc[u] = len(disc) + 1
        skipped = False
        for v in adj[u]:
            if v not in disc:
                out.append((u, v))                    # a tree road, pointing down
                visit(v, u)
            elif v == parent and not skipped:
                skipped = True                        # the road we arrived along, already directed
            elif disc[v] < disc[u]:
                out.append((u, v))                    # a back road (or parallel road), pointing up
    for s in adj:
        if s not in disc:
            visit(s, None)
    return out


def pieces_after_removal(adj: dict) -> dict:
    """Thinking Problem 2: for every place u, the number of pieces that u's own piece falls into when u (and its
    roads) is removed, from one DFS: the root gives one piece per DFS child; any other place gives the piece above
    it plus one piece per child v with low[v] >= disc[u]. Cut vertices are the places with a count of 2 or more."""
    disc, low, count = {}, {}, {}

    def visit(u, parent):
        disc[u] = low[u] = len(disc) + 1
        count[u], skipped = (0 if parent is None else 1), False
        for v in adj[u]:
            if v not in disc:
                visit(v, u)
                low[u] = min(low[u], low[v])
                if parent is None or low[v] >= disc[u]:
                    count[u] += 1
            elif v == parent and not skipped:
                skipped = True
            else:
                low[u] = min(low[u], disc[v])
    for s in adj:
        if s not in disc:
            visit(s, None)
    return count


def weak_links_low_bug(adj: dict) -> dict:
    """Thinking Problem 3, the FLAWED variant: a back road updates low[u] with low[v] instead of disc[v].
    Bridges stay right; cut vertices can be missed."""
    disc, low, bridges, cuts = {}, {}, [], set()

    def visit(u, parent):
        disc[u] = low[u] = len(disc) + 1
        children, skipped = 0, False
        for v in adj[u]:
            if v not in disc:
                children += 1
                visit(v, u)
                low[u] = min(low[u], low[v])
                if low[v] > disc[u]:
                    bridges.append((u, v))
                if parent is not None and low[v] >= disc[u]:
                    cuts.add(u)
            elif v == parent and not skipped:
                skipped = True
            else:
                low[u] = min(low[u], low[v])          # the bug: should be disc[v]
        if parent is None and children >= 2:
            cuts.add(u)
    for s in adj:
        if s not in disc:
            visit(s, None)
    return {"disc": disc, "low": low, "bridges": bridges, "cuts": sorted(cuts, key=disc.get)}


BOWTIE = adjacency("ABCDE", [("A", "B"), ("B", "C"), ("C", "A"), ("C", "D"), ("D", "E"), ("E", "C")])

if __name__ == "__main__":
    town = adjacency(PLACES, ROADS)
    print(one_way_plan(town))
    print(one_way_plan(adjacency(PLACES + OUTER, ROADS + OUTER_ROADS)))
    print(pieces_after_removal(adjacency(PLACES + OUTER, ROADS + OUTER_ROADS)))
    print(weak_links(BOWTIE), weak_links_low_bug(BOWTIE))
