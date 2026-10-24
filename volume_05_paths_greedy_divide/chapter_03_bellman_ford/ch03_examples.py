"""Volume 5, Chapter 3 - Negative Roads: Bellman-Ford relaxes every road, round after round.

Run:  python3 ch03_examples.py
"""

from __future__ import annotations

# The courier's one-way legs between depots: a negative weight is a bonus paid for carrying a parcel.
DEPOTS = ["A", "B", "C", "D", "E"]
LEGS = [("A", "B", 6), ("A", "C", 7), ("B", "C", 8), ("B", "D", 5), ("B", "E", -4), ("C", "D", -3), ("C", "E", 9),
        ("D", "B", -2), ("E", "D", 7), ("E", "A", 2)]


def bellman_ford(vertices: list, edges: list, start, log: list | None = None) -> tuple[dict, dict, bool]:
    """Shortest distances with negative weights allowed (the rounds table of Section 3.4).
    Returns (dist, parent, has_negative_cycle). Up to V - 1 rounds, then one extra round to detect a cycle."""
    inf = float("inf")
    dist = {v: inf for v in vertices}
    parent = {v: None for v in vertices}
    dist[start] = 0
    for rnd in range(1, len(vertices)):
        changed = False
        for a, b, w in edges:
            if dist[a] + w < dist[b]:
                dist[b] = dist[a] + w
                parent[b] = a
                changed = True
        if log is not None:
            log.append((rnd, dict(dist)))
        if not changed:
            break                                     # nothing improved: every distance is final
    cycle = any(dist[a] + w < dist[b] for a, b, w in edges)
    return dist, parent, cycle


def route(parent: dict, goal) -> list:
    out = []
    while goal is not None:
        out.append(goal)
        goal = parent[goal]
    return out[::-1]


def find_negative_cycle(vertices: list, edges: list) -> list | None:
    """Return one negative cycle as a list of vertices in travel order (first vertex not repeated), or None.
    Every vertex starts at 0, as if a new start joined each by a 0-cost leg, so cycles anywhere are found.
    A vertex still improved in round V lies on, or downstream of, a cycle; V parent steps back land inside it."""
    if not vertices:
        return None
    dist = {v: 0 for v in vertices}
    parent = {v: None for v in vertices}
    last = None
    for _ in range(len(vertices)):
        last = None
        for a, b, w in edges:
            if dist[a] + w < dist[b]:
                dist[b] = dist[a] + w
                parent[b] = a
                last = b
        if last is None:
            return None                               # a round with no change: no negative cycle
    v = last
    for _ in range(len(vertices)):
        v = parent[v]                                 # now certainly on the cycle
    cycle, u = [v], parent[v]
    while u != v:
        cycle.append(u)
        u = parent[u]
    return cycle[::-1]


def spfa(vertices: list, edges: list, start) -> tuple[dict, int]:
    """Bellman-Ford that relaxes only the legs of vertices whose cost changed (a queue of 'dirty' vertices).
    Assumes no negative cycle is reachable. Returns (dist, legs examined)."""
    out = {v: [] for v in vertices}
    for a, b, w in edges:
        out[a].append((b, w))
    inf = float("inf")
    dist = {v: inf for v in vertices}
    dist[start] = 0
    queue, waiting, examined = [start], {start}, 0
    while queue:
        a = queue.pop(0)
        waiting.discard(a)
        for b, w in out[a]:
            examined += 1
            if dist[a] + w < dist[b]:
                dist[b] = dist[a] + w
                if b not in waiting:
                    queue.append(b)
                    waiting.add(b)
    return dist, examined


def cheapest_leg_counts(parent: dict, start) -> dict:
    """How many legs each vertex's cheapest route (by parent links) uses: round k is guaranteed to fix every
    vertex whose count is at most k (Section 3.4)."""
    out = {}
    for v in parent:
        n, u = 0, v
        while u != start and u is not None:
            u, n = parent[u], n + 1
        out[v] = n if u == start else None
    return out


def cheapest_within(vertices: list, edges: list, start, k: int) -> dict:
    """Cheapest cost from start using at most k legs (Challenge 3.1): k rounds, each computed only from the costs at
    the start of the round, so no round can use more than one new leg."""
    dist = {v: float("inf") for v in vertices}
    dist[start] = 0
    for _ in range(k):
        old = dict(dist)
        for a, b, w in edges:
            if old[a] + w < dist[b]:
                dist[b] = old[a] + w
    return dist


# Difference constraints (Section 3.6): "later - earlier <= limit", in minutes after the festival opens
FESTIVAL = [("Talk", "Setup", -30),     # Setup - Talk <= -30: the talk starts at least 30 after setup
            ("Setup", "Quiz", 60),      # Quiz - Setup <= 60: the quiz starts at most 60 after setup
            ("Quiz", "Talk", -20),      # Talk - Quiz <= -20: the quiz starts at least 20 after the talk
            ("Lunch", "Quiz", -15),     # Quiz - Lunch <= -15: lunch at least 15 after the quiz
            ("Setup", "Lunch", 90)]     # Lunch - Setup <= 90: lunch at most 90 after setup


def difference_constraints(rules: list) -> dict | None:
    """Each rule (i, j, w) means x[j] - x[i] <= w, an arrow i -> j of length w. Add a start joined to every event
    by length 0 and run Bellman-Ford: the distances satisfy every rule, and a negative cycle means none can."""
    events = sorted({r[0] for r in rules} | {r[1] for r in rules})
    edges = [("start", e, 0) for e in events] + list(rules)
    dist, _, cycle = bellman_ford(["start"] + events, edges, "start")
    if cycle:
        return None
    shift = -min(dist[e] for e in events)                 # move every time so the earliest is 0
    return {e: dist[e] + shift for e in events}


if __name__ == "__main__":
    log = []
    dist, parent, cycle = bellman_ford(DEPOTS, LEGS, "A", log)
    for rnd, d in log:
        print(rnd, d)
    print(dist, cycle, route(parent, "D"), route(parent, "E"))
    print(difference_constraints(FESTIVAL), difference_constraints(FESTIVAL[:1] + [("Setup", "Quiz", 40)] + FESTIVAL[2:]))
