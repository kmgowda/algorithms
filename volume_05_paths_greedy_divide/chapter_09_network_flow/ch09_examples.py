"""Volume 5, Chapter 9 - Network Flow: as much as possible through limited roads (Edmonds-Karp).

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
    """Fill any path with spare room, trying roads in list order, and never push flow back (Figure 9.4).
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
    """The places reachable from s in the final residual graph, and the full edges leaving them (Section 9.5)."""
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


def residual(edges: list, flow: dict) -> dict:
    """The residual graph of a flow (Figure 9.3): spare room forwards, and room to cancel backwards.
    Returns {(a, b): room} for every pair with room > 0."""
    room = {}
    for a, b, c in edges:
        room[(a, b)] = room.get((a, b), 0) + c - flow[(a, b)]
        room[(b, a)] = room.get((b, a), 0) + flow[(a, b)]
    return {e: r for e, r in room.items() if r > 0}


def flow_after_rounds(nodes: list, edges: list, s, t, rounds: int) -> dict:
    """The flow on each edge after the first `rounds` augmenting paths of Edmonds-Karp (Figure 9.2)."""
    log = []
    max_flow(nodes, edges, s, t, log)
    flow = {(a, b): 0 for a, b, _ in edges}
    for path, push in log[:rounds]:
        for a, b in zip(path, path[1:]):
            if (a, b) in flow and flow[(a, b)] + push <= dict(((x, y), c) for x, y, c in edges)[(a, b)]:
                flow[(a, b)] += push
            else:
                flow[(b, a)] -= push                    # the path used a backward edge: cancel flow
    return flow


def ford_fulkerson(nodes: list, edges: list, s, t, choose: str = "fewest") -> tuple[int, int]:
    """The Ford-Fulkerson method with a chosen rule for picking the augmenting path (Section 9.4).
    choose = "fewest": fewest roads (Edmonds-Karp); "smallest": the path with the smallest bottleneck, the
    worst possible choice. Returns (total flow, number of rounds)."""
    room = {}
    for a, b, c in edges:
        room[(a, b)] = room.get((a, b), 0) + c
        room.setdefault((b, a), 0)
    total = rounds = 0
    while True:
        paths = []

        def walk(v, path, seen):
            if v == t:
                paths.append(list(path))
                return
            for (a, b), r in room.items():
                if a == v and r > 0 and b not in seen:
                    path.append((a, b))
                    walk(b, path, seen | {b})
                    path.pop()

        walk(s, [], {s})
        if not paths:
            return total, rounds
        if choose == "fewest":
            path = min(paths, key=len)
        else:
            path = min(paths, key=lambda p: (min(room[e] for e in p), -len(p)))
        push = min(room[e] for e in path)
        for a, b in path:
            room[(a, b)] -= push
            room[(b, a)] += push
        total += push
        rounds += 1


def decompose(edges: list, flow: dict, s, t) -> list:
    """Split a flow into source-to-sink paths, each with the boxes it carries (Section 9.5)."""
    left = dict(flow)
    out = []
    while True:
        path, v, seen = [s], s, {s}
        while v != t:
            nxt = next((b for (a, b), f in left.items() if a == v and f > 0 and b not in seen), None)
            if nxt is None:
                return out
            path.append(nxt)
            seen.add(nxt)
            v = nxt
        push = min(left[(a, b)] for a, b in zip(path, path[1:]))
        for a, b in zip(path, path[1:]):
            left[(a, b)] -= push
        out.append((path, push))


def edge_disjoint_paths(nodes: list, edges: list, s, t) -> list:
    """Routes from s to t that share no road (Menger): give every road capacity 1, find a maximum flow, and split it
    into paths."""
    unit = [(a, b, 1) for a, b, *_ in edges]
    _, flow = max_flow(nodes, unit, s, t)
    return [p for p, _ in decompose(unit, flow, s, t)]


# Project selection: each project earns money but needs some equipment, and each piece of equipment costs money.
PROJECTS = {"Reading app": 8, "Coding club": 6, "Film night": 2}
EQUIPMENT = {"Wi-Fi": 5, "Tablets": 6, "Projector": 3}
NEEDS = {"Reading app": ["Wi-Fi", "Tablets"], "Coding club": ["Tablets"], "Film night": ["Projector"]}


def project_selection(projects: dict, equipment: dict, needs: dict) -> tuple[int, list]:
    """Choose projects to maximise profit = earnings - equipment bought, by one minimum cut (Section 9.7).
    Source -> project (its earnings), equipment -> sink (its cost), project -> equipment it needs (unlimited).
    The projects on the source side of the minimum cut are the ones to run."""
    s, t = "source", "sink"
    big = sum(projects.values()) + 1                    # "unlimited": larger than any cut worth taking
    edges = [(s, p, e) for p, e in projects.items()] + [(q, t, c) for q, c in equipment.items()]
    edges += [(p, q, big) for p, qs in needs.items() for q in qs]
    nodes = [s, *projects, *equipment, t]
    cut_value, _ = max_flow(nodes, edges, s, t)
    side, _ = min_cut(nodes, edges, s, t)
    return sum(projects.values()) - cut_value, [p for p in projects if p in side]


def best_projects_brute(projects: dict, equipment: dict, needs: dict) -> int:
    """Try every set of projects (2^n of them) and keep the best profit."""
    names, best = list(projects), 0
    for mask in range(1 << len(names)):
        chosen = [names[i] for i in range(len(names)) if mask >> i & 1]
        kit = {q for p in chosen for q in needs[p]}
        best = max(best, sum(projects[p] for p in chosen) - sum(equipment[q] for q in kit))
    return best


if __name__ == "__main__":
    log = []
    total, flow = max_flow(NODES, PIPES, "Warehouse", "Library", log)
    print(total)
    for row in log:
        print(row)
    print(flow)
    print(min_cut(NODES, PIPES, "Warehouse", "Library"))
