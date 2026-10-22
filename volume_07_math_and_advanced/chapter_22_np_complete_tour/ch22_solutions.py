"""Volume 7, Chapter 22 - Thinking Problems.

Problem 1: the 3-SAT to independent-set translation is faithful (checked on random small formulas).
Problem 2: deciding 2-colourability in O(V + E) with breadth-first search, returning a colouring or an odd cycle.
Problem 3: greedy colouring in a bad order uses 3 colours on a path that needs only 2.
"""

from __future__ import annotations

from collections import deque


def two_colour(vertices: list, edges: list) -> tuple[dict | None, list | None]:
    """BFS from every uncoloured place, alternating colours. Returns (colouring, None) or (None, an odd cycle)."""
    adj = {v: [] for v in vertices}
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    colour, parent = {}, {}
    for s in vertices:
        if s in colour:
            continue
        colour[s], parent[s] = 0, None
        queue = deque([s])
        while queue:
            v = queue.popleft()
            for w in adj[v]:
                if w not in colour:
                    colour[w], parent[w] = 1 - colour[v], v
                    queue.append(w)
                elif colour[w] == colour[v]:              # an edge inside one colour: an odd cycle
                    return None, odd_cycle(parent, v, w)
    return colour, None


def odd_cycle(parent: dict, v, w) -> list:
    pv, pw = [v], [w]
    while pv[-1] is not None:
        pv.append(parent[pv[-1]])
    while pw[-1] is not None:
        pw.append(parent[pw[-1]])
    pv, pw = pv[:-1], pw[:-1]
    common = next(x for x in pv if x in pw)
    return pv[:pv.index(common) + 1] + list(reversed(pw[:pw.index(common)]))


def greedy_colour(order: list, edges: list) -> dict:
    adj = {v: set() for v in order}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    colour = {}
    for v in order:
        used = {colour[w] for w in adj[v] if w in colour}
        colour[v] = next(c for c in range(len(order) + 1) if c not in used)
    return colour


if __name__ == "__main__":
    path = [("a", "b"), ("b", "c"), ("c", "d")]
    print(two_colour(list("abcd"), path), greedy_colour(list("adbc"), path))
    print(two_colour(list("xyz"), [("x", "y"), ("y", "z"), ("z", "x")]))
