"""Volume 5, Chapter 10 - Push-Relabel: maximum flow by local pushes and rising heights.

Run:  python3 ch10_examples.py
"""

from __future__ import annotations

import random
from collections import deque

# Chapter 9's network: boxes of books per hour that each one-way road can carry.
NODES = ["Warehouse", "Docks", "Mill", "Bridge", "Square", "Library"]
PIPES = [("Warehouse", "Docks", 10), ("Warehouse", "Mill", 8), ("Docks", "Mill", 2), ("Docks", "Bridge", 5),
         ("Mill", "Square", 9), ("Bridge", "Library", 7), ("Square", "Bridge", 3), ("Square", "Library", 6)]


class CountingRoom(dict):
    """A room table that counts how often it is read: the work measure of Section 10.6."""
    reads = 0

    def __getitem__(self, key):
        CountingRoom.reads += 1
        return super().__getitem__(key)


ROOM_TYPE = dict                                       # compare() swaps in CountingRoom


def residual_room(nodes: list, edges: list) -> tuple[dict, dict]:
    """Room on every road and on its reverse (0 at first), and each place's list of neighbours."""
    room = ROOM_TYPE()
    for a, b, c in edges:
        room[(a, b)] = room.get((a, b), 0) + c
        room.setdefault((b, a), 0)
    adj = {v: [] for v in nodes}
    for a, b in room:
        adj[a].append(b)
    return room, adj


def flood(s, t, room: dict, adj: dict, excess: dict, log: list | None) -> deque:
    """Fill every road out of the source to capacity; return the places that now hold excess."""
    active = deque()
    for v in adj[s]:
        amount = room[(s, v)]
        if amount > 0:
            room[(s, v)] -= amount
            room[(v, s)] += amount
            excess[v] += amount
            excess[s] -= amount
            if log is not None:
                log.append(("push", s, v, amount))
            if v != t:
                active.append(v)
    return active


def push_relabel(nodes: list, edges: list, s, t, log: list | None = None) -> tuple[int, dict, dict]:
    """FIFO push-relabel (Section 10.4). Returns (total flow, flow on each original edge, final heights).
    log, if given, receives ("push", u, v, amount) and ("relabel", u, old height, new height) steps."""
    room, adj = residual_room(nodes, edges)
    height = {v: 0 for v in nodes}
    height[s] = len(nodes)                             # the source stands n levels up
    excess = {v: 0 for v in nodes}
    active = flood(s, t, room, adj, excess, log)
    while active:
        discharge(active.popleft(), s, t, room, adj, height, excess, active, log)
    flow = {(a, b): max(0, c - room[(a, b)]) for a, b, c in edges}
    return excess[t], flow, height


def discharge(u, s, t, room: dict, adj: dict, height: dict, excess: dict, active: deque, log: list | None) -> None:
    """Push u's excess downhill, one step at a time; relabel u when no road leads exactly one level down."""
    while excess[u] > 0:
        for v in adj[u]:
            if room[(u, v)] > 0 and height[u] == height[v] + 1:
                amount = min(excess[u], room[(u, v)])
                room[(u, v)] -= amount
                room[(v, u)] += amount
                excess[u] -= amount
                excess[v] += amount
                if log is not None:
                    log.append(("push", u, v, amount))
                if v not in (s, t) and excess[v] == amount:
                    active.append(v)                   # v has just become active
                if excess[u] == 0:
                    return
        old = height[u]
        height[u] = 1 + min(height[v] for v in adj[u] if room[(u, v)] > 0)
        if log is not None:
            log.append(("relabel", u, old, height[u]))


def exact_heights(nodes: list, room: dict, adj: dict, s, t) -> dict:
    """Global relabelling (Section 10.6): each place's height becomes its true number of roads to t in the residual
    graph, found by one breadth-first search backwards from t; places that cannot reach t are measured to s and
    lifted above len(nodes)."""
    n = len(nodes)
    height = {v: 2 * n for v in nodes}
    for root, base in ((t, 0), (s, n)):
        if height[root] < 2 * n:
            continue
        height[root] = base
        queue = deque([root])
        while queue:
            v = queue.popleft()
            for u in adj[v]:
                if height[u] == 2 * n and room[(u, v)] > 0:
                    height[u] = height[v] + 1
                    queue.append(u)
    height[s] = n
    return height


def push_relabel_global(nodes: list, edges: list, s, t, every: int | None = None) -> tuple[int, int, int]:
    """FIFO push-relabel with global relabelling after every `every` relabels (default: once per place).
    Returns (total flow, pushes, relabels)."""
    room, adj = residual_room(nodes, edges)
    excess = {v: 0 for v in nodes}
    log, since = [], 0
    active = flood(s, t, room, adj, excess, log)
    height = exact_heights(nodes, room, adj, s, t)
    every = every or len(nodes)
    while active:
        u = active.popleft()
        before = len(log)
        discharge(u, s, t, room, adj, height, excess, active, log)
        since += sum(1 for step in log[before:] if step[0] == "relabel")
        if since >= every:
            height, since = exact_heights(nodes, room, adj, s, t), 0
    pushes, relabels = counts(log)
    return excess[t], pushes, relabels


def counts(log: list) -> tuple[int, int]:
    """(number of pushes, number of relabels) in a log."""
    pushes = sum(1 for step in log if step[0] == "push")
    return pushes, len(log) - pushes


def cut_from_heights(nodes: list, edges: list, s, t) -> tuple[set, list]:
    """After push-relabel, the places that can still send to t in the residual graph lie on the sink's side; the
    rest form the source's side of a minimum cut (Section 10.5)."""
    _, flow, _ = push_relabel(nodes, edges, s, t)
    room = {}
    for a, b, c in edges:
        room[(a, b)] = room.get((a, b), 0) + c - flow[(a, b)]
        room[(b, a)] = room.get((b, a), 0) + flow[(a, b)]
    sink_side, stack = {t}, [t]
    while stack:
        v = stack.pop()
        for (a, b), r in room.items():
            if b == v and r > 0 and a not in sink_side:
                sink_side.add(a)
                stack.append(a)
    side = set(nodes) - sink_side
    return side, [(a, b, c) for a, b, c in edges if a in side and b not in side]


def edmonds_karp(nodes: list, edges: list, s, t) -> tuple[int, int, dict]:
    """Chapter 9's Edmonds-Karp on the same room table: (total flow, augmenting paths, the final room)."""
    room, adj = residual_room(nodes, edges)
    total = paths = 0
    while True:
        parent, queue = {s: None}, deque([s])
        while queue and t not in parent:
            v = queue.popleft()
            for w in adj[v]:
                if w not in parent and room[(v, w)] > 0:
                    parent[w] = v
                    queue.append(w)
        if t not in parent:
            return total, paths, room
        path, v = [], t
        while parent[v] is not None:
            path.append((parent[v], v))
            v = parent[v]
        push = min(room[e] for e in path)
        for a, b in path:
            room[(a, b)] -= push
            room[(b, a)] += push
        total += push
        paths += 1


def layered_network(layers: int, width: int, seed: int = 0) -> tuple[list, list]:
    """A test network: a source, `layers` columns of `width` places, a sink; every place joins each place of the
    next column with a random capacity from 1 to 20."""
    rng = random.Random(seed)
    cols = [["s"]] + [[f"v{i}_{j}" for j in range(width)] for i in range(layers)] + [["t"]]
    edges = [(a, b, rng.randint(1, 20)) for c1, c2 in zip(cols, cols[1:]) for a in c1 for b in c2]
    return [v for c in cols for v in c], edges


def compare(nodes: list, edges: list, s="s", t="t") -> dict:
    """Run both methods on one network and report the flow and the work each did, measured as reads of the
    room table (every look at a road's spare room)."""
    global ROOM_TYPE
    ROOM_TYPE = CountingRoom
    try:
        log, rooms = [], []
        total, _, _ = push_relabel(nodes, edges, s, t, log)
        pr_reads = CountingRoom.reads
        CountingRoom.reads = 0
        ek_total, ek_paths, _ = edmonds_karp(nodes, edges, s, t)
        ek_reads = CountingRoom.reads
        CountingRoom.reads = 0
        g_total, g_pushes, g_relabels = push_relabel_global(nodes, edges, s, t)
        g_reads = CountingRoom.reads
    finally:
        ROOM_TYPE = dict
        CountingRoom.reads = 0
    pushes, relabels = counts(log)
    return {"places": len(nodes), "roads": len(edges), "flow": total, "same": total == ek_total == g_total,
            "ek_paths": ek_paths, "ek_reads": ek_reads, "pushes": pushes, "relabels": relabels, "pr_reads": pr_reads,
            "global_pushes": g_pushes, "global_relabels": g_relabels, "global_reads": g_reads}


if __name__ == "__main__":
    log = []
    total, flow, height = push_relabel(NODES, PIPES, "Warehouse", "Library", log)
    print(total, counts(log), height)
    for step in log:
        print(step)
    print(flow)
    print(cut_from_heights(NODES, PIPES, "Warehouse", "Library"))
    print(compare(NODES, PIPES, "Warehouse", "Library"))
    for L, W in [(3, 3), (5, 5), (8, 8), (10, 12)]:
        print(L, W, compare(*layered_network(L, W)))
