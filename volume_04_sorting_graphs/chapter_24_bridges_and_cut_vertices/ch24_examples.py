"""Volume 4, Chapter 24 - Weak Links: Bridges and Cut Vertices, found with one DFS and low-links.

Run:  python3 ch24_examples.py
"""

from __future__ import annotations

from collections import deque

PLACES = ["Library", "School", "Park", "Market", "Station", "Museum", "Hospital", "Harbour"]
ROADS = [("Library", "School"), ("Library", "Park"), ("School", "Market"), ("Park", "Market"), ("School", "Station"),
         ("Market", "Station"), ("Market", "Museum"), ("Park", "Hospital"), ("Hospital", "Museum"),
         ("Station", "Harbour"), ("Museum", "Harbour"), ("Station", "Museum")]
# the district beyond the town: one lane to the Lighthouse, one track to the Farm
OUTER = ["Lighthouse", "Farm"]
OUTER_ROADS = [("Harbour", "Lighthouse"), ("Hospital", "Farm")]


def adjacency(places, roads) -> dict:
    adj = {p: [] for p in places}
    for a, b in roads:
        adj[a].append(b)
        adj[b].append(a)
    return adj


def road_ids(adj: dict) -> dict:
    """Give every road a number of its own, so that two parallel roads between the same places stay different:
    {place: [(neighbour, road number), ...]} in neighbour-list order. The k-th copy of w in u's list and the k-th
    copy of u in w's list are the same road (adjacency() adds both ends together); a self-loop appears twice."""
    out, waiting, loops, count = {u: [] for u in adj}, {}, {}, 0
    for u in adj:
        for w in adj[u]:
            if u == w:                                   # the two copies of a self-loop share one number
                if loops.get(u) is not None:
                    rid, loops[u] = loops[u], None
                else:
                    rid, count = count, count + 1
                    loops[u] = rid
            elif waiting.get((w, u)):
                rid = waiting[(w, u)].popleft()          # the other end of a road already numbered
            else:
                rid, count = count, count + 1
                waiting.setdefault((u, w), deque()).append(rid)
            out[u].append((w, rid))
    return out


def weak_links(adj: dict) -> dict:
    """Bridges and cut vertices from one DFS with discovery times and low-links (Figure 24.3)."""
    disc, low, bridges, cuts = {}, {}, [], set()
    def visit(u, parent):
        disc[u] = low[u] = len(disc) + 1                # the next discovery time
        children, skipped = 0, False
        for v in adj[u]:
            if v not in disc:                           # a tree road u-v
                children += 1
                visit(v, u)
                low[u] = min(low[u], low[v])
                if low[v] > disc[u]:
                    bridges.append((u, v))
                if parent is not None and low[v] >= disc[u]:
                    cuts.add(u)
            elif v == parent and not skipped:
                skipped = True                          # the one road we arrived along
            else:
                low[u] = min(low[u], disc[v])           # a back road, or a parallel road
        if parent is None and children >= 2:
            cuts.add(u)
    for s in adj:
        if s not in disc:
            visit(s, None)
    return {"disc": disc, "low": low, "bridges": bridges, "cuts": sorted(cuts, key=disc.get)}


def blocks(adj: dict) -> list[list]:
    """Biconnected components ("blocks", Section 24.5): the same DFS, plus a stack of roads. A tree road is pushed
    when it is followed, a back road when it is first seen from its lower end; when a child v of u has
    low[v] >= disc[u], the roads down to (u, v) form one block. Returns each block as a list of roads (u, v) in the
    order they were popped; self-loops are left out."""
    disc, low, parent = {}, {}, {}
    road_stack, out = [], []
    time = [0]

    def visit(u):
        time[0] += 1
        disc[u] = low[u] = time[0]
        skipped = False
        for v in adj[u]:
            if v == u:
                continue
            if v not in disc:
                parent[v] = u
                road_stack.append((u, v))
                visit(v)
                low[u] = min(low[u], low[v])
                if low[v] >= disc[u]:                     # u separates v's subtree: pop one block
                    block = []
                    while True:
                        e = road_stack.pop()
                        block.append(e)
                        if e == (u, v):
                            break
                    out.append(block)
            elif v == parent.get(u) and not skipped:
                skipped = True
            elif disc[v] < disc[u]:                       # a back road, seen from its lower end
                road_stack.append((u, v))
                low[u] = min(low[u], disc[v])

    for s in adj:
        if s not in disc:
            parent[s] = None
            visit(s)
    return out


def block_places(block: list) -> set:
    return {p for e in block for p in e}


def block_cut_tree(adj: dict) -> tuple[list[set], list[tuple]]:
    """The block-cut tree: one node per block and one per cut vertex, joined when the cut vertex lies in the block.
    Returns (the blocks as sets of places, the joins as (block index, cut vertex))."""
    bs = [block_places(b) for b in blocks(adj)]
    cuts = weak_links(adj)["cuts"]
    return bs, [(i, c) for i, b in enumerate(bs) for c in cuts if c in b]


def brute_force(adj: dict) -> dict:
    """Check by removal: a road (one copy, if there are parallel roads) is a bridge if removing it increases the
    number of pieces; a place is a cut vertex if removing it (and its roads) increases the number of pieces."""
    ids = road_ids(adj)

    def pieces(skip_place=None, skip_road=None):
        seen, n = set(), 0
        for s in adj:
            if s == skip_place or s in seen:
                continue
            n += 1
            stack = [s]
            seen.add(s)
            while stack:
                v = stack.pop()
                for w, rid in ids[v]:
                    if w == skip_place or rid == skip_road or w in seen:
                        continue
                    seen.add(w)
                    stack.append(w)
        return n
    base = pieces()
    roads = {rid for u in ids for w, rid in ids[u] if u != w}
    bridge_ids = {r for r in roads if pieces(skip_road=r) > base}
    ends = {rid: frozenset((u, w)) for u in ids for w, rid in ids[u]}
    return {"bridges": {ends[r] for r in bridge_ids},
            "cuts": {p for p in adj if pieces(skip_place=p) > base - (1 if not adj[p] else 0)}}


if __name__ == "__main__":
    town = adjacency(PLACES, ROADS)
    r = weak_links(town)
    print(r["bridges"], r["cuts"])
    big = adjacency(PLACES + OUTER, ROADS + OUTER_ROADS)
    r = weak_links(big)
    print(r["bridges"], r["cuts"])
    print({p: (r["disc"][p], r["low"][p]) for p in sorted(r["disc"], key=r["disc"].get)})
    print(brute_force(big))
    print([sorted(block_places(b)) for b in blocks(big)])
    bow = adjacency("ABCDE", [("A", "B"), ("B", "C"), ("C", "A"), ("C", "D"), ("D", "E"), ("E", "C")])
    print(blocks(bow), block_cut_tree(bow))
    print(weak_links(adjacency("AB", [("A", "B"), ("A", "B")])))
