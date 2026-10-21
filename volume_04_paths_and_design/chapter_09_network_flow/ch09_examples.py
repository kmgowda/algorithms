"""Volume 4, Chapter 9 - Network Flow: as much as possible through limited roads (Edmonds-Karp).

Run:  python3 ch09_examples.py
"""

from __future__ import annotations

from collections import deque

# Boxes of books per hour that each one-way road can carry from the Warehouse to the Library.
NODES = ["Warehouse", "Docks", "Mill", "Bridge", "Square", "Library"]
PIPES = [("Warehouse", "Docks", 10), ("Warehouse", "Mill", 8), ("Docks", "Mill", 2), ("Docks", "Bridge", 5),
         ("Mill", "Square", 9), ("Bridge", "Library", 7), ("Square", "Bridge", 3), ("Square", "Library", 6)]


def max_flow(nodes: list, edges: list, s, t, log: list | None = None) -> tuple[int, dict]:
    """Edmonds-Karp (Figure 9.2): push flow along shortest augmenting paths in the residual graph.
    Returns (total flow, flow on each original edge)."""
    cap = {}
    for a, b, c in edges:
        cap[(a, b)] = cap.get((a, b), 0) + c
        cap.setdefault((b, a), 0)                      # room to push flow back
    adj = {v: [] for v in nodes}
    for a, b in cap:
        adj[a].append(b)
    total = 0
    while True:
        parent, queue = {s: None}, deque([s])
        while queue and t not in parent:               # breadth-first search for a path with spare room
            v = queue.popleft()
            for w in adj[v]:
                if w not in parent and cap[(v, w)] > 0:
                    parent[w] = v
                    queue.append(w)
        if t not in parent:
            break
        path, v = [], t
        while parent[v] is not None:
            path.append((parent[v], v))
            v = parent[v]
        push = min(cap[e] for e in path)
        for a, b in path:
            cap[(a, b)] -= push
            cap[(b, a)] += push
        total += push
        if log is not None:
            log.append(([a for a, _ in reversed(path)] + [t], push))
    flow = {(a, b): c - cap[(a, b)] for a, b, c in edges}
    return total, flow


def greedy_no_undo(edges: list, s, t) -> int:
    """Fill any path with spare room, trying roads in list order, and never push flow back (Section 9.4).
    It can get stuck below the maximum."""
    room = {(a, b): c for a, b, c in edges}

    def find(v, seen):
        if v == t:
            return []
        for a, b, _ in edges:
            if a == v and room[(a, b)] > 0 and b not in seen:
                rest = find(b, seen | {b})
                if rest is not None:
                    return [(a, b)] + rest
        return None

    total = 0
    while (path := find(s, {s})) is not None:
        push = min(room[x] for x in path)
        for x in path:
            room[x] -= push
        total += push
    return total


def min_cut(nodes: list, edges: list, s, t) -> tuple[set, list]:
    """The places reachable from s in the final residual graph, and the full edges leaving them (Figure 9.3)."""
    _, flow = max_flow(nodes, edges, s, t)
    room = {}
    for a, b, c in edges:
        room[(a, b)] = room.get((a, b), 0) + c - flow[(a, b)]
        room[(b, a)] = room.get((b, a), 0) + flow[(a, b)]
    seen, stack = {s}, [s]
    while stack:
        v = stack.pop()
        for (a, b), r in room.items():
            if a == v and r > 0 and b not in seen:
                seen.add(b)
                stack.append(b)
    return seen, [(a, b, c) for a, b, c in edges if a in seen and b not in seen]


if __name__ == "__main__":
    log = []
    total, flow = max_flow(NODES, PIPES, "Warehouse", "Library", log)
    print(total)
    for row in log:
        print(row)
    print(flow)
    print(min_cut(NODES, PIPES, "Warehouse", "Library"))
