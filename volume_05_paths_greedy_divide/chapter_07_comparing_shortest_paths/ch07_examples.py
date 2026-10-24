"""Volume 5, Chapter 7 - Every Shortest-Path Algorithm on One Map.

Runs the methods of Chapters 1-6 on the same inputs and compares answers, work, and time.
Run:  python3 ch07_examples.py
"""

from __future__ import annotations

import importlib.util
import os
import heapq
import random
import time

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(folder: str, name: str):
    spec = importlib.util.spec_from_file_location(name + "_v4", os.path.join(HERE, "..", folder, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


brute = _load("chapter_01_shortest_path_problem", "ch01_examples")
dij = _load("chapter_02_dijkstra", "ch02_examples")
bf = _load("chapter_03_bellman_ford", "ch03_examples")
fw = _load("chapter_05_floyd_warshall", "ch05_examples")
ast = _load("chapter_06_a_star", "ch06_examples")


def town_answers() -> dict:
    """Library-to-Harbour minutes from every method."""
    adj = dij.weighted_adjacency()
    edges = [(a, b, w) for a, b, w in dij.ROADS] + [(b, a, w) for a, b, w in dij.ROADS]
    s = ast.speed_limit()
    fwd, _ = fw.town_table()
    return {
        "brute force": brute.shortest_by_brute_force(adj, "Library", "Harbour")[0],
        "Dijkstra": dij.dijkstra(adj, "Library")[0]["Harbour"],
        "Bellman-Ford": bf.bellman_ford(dij.PLACES, edges, "Library")[0]["Harbour"],
        "Floyd-Warshall": fwd[0][7],
        "A*": ast.a_star(adj, "Library", "Harbour", lambda v: s * ast.crow_flies(v, "Harbour"))[0],
    }


def random_map(n: int, m: int, seed: int = 1, low: int = 1) -> tuple[dict, list]:
    rng = random.Random(seed)
    adj = {i: {} for i in range(n)}
    edges = []
    while len(edges) < m:
        a, b = rng.randrange(n), rng.randrange(n)
        if a != b and b not in adj[a]:
            w = rng.randint(low, 20)
            adj[a][b] = adj[b][a] = w
            edges += [(a, b, w), (b, a, w)]
    return adj, edges


def timings(n: int, m: int, seed: int = 1) -> dict:
    """Milliseconds for one-source answers (and all pairs for Floyd-Warshall) on a random map."""
    adj, edges = random_map(n, m, seed)
    out = {}
    t = time.perf_counter(); d1 = dij.dijkstra(adj, 0)[0]; out["Dijkstra"] = (time.perf_counter() - t) * 1000
    t = time.perf_counter(); d2 = bf.bellman_ford(list(range(n)), edges, 0)[0]; out["Bellman-Ford"] = (time.perf_counter() - t) * 1000
    t = time.perf_counter(); d3 = fw.floyd_warshall(n, [(a, b, w) for a, b, w in edges], directed=True)[0]
    out["Floyd-Warshall (all pairs)"] = (time.perf_counter() - t) * 1000
    assert all(d1.get(v, float("inf")) == d2[v] == d3[0][v] for v in range(n))
    return {k: round(v, 1) for k, v in out.items()}


def one_source(n: int, m: int, seed: int = 1) -> dict:
    """Milliseconds for one start: Dijkstra against Bellman-Ford (Figure 7.1)."""
    adj, edges = random_map(n, m, seed)
    t = time.perf_counter(); a = dij.dijkstra(adj, 0)[0]; td = (time.perf_counter() - t) * 1000
    t = time.perf_counter(); b = bf.bellman_ford(list(range(n)), edges, 0)[0]; tb = (time.perf_counter() - t) * 1000
    assert all(a.get(v, float("inf")) == b[v] for v in range(n))
    return {"Dijkstra": round(td, 1), "Bellman-Ford": round(tb, 1)}


def all_pairs(n: int, m: int, seed: int = 1) -> dict:
    """Milliseconds for every pair: Dijkstra from each place against Floyd-Warshall (Figure 7.1)."""
    adj, edges = random_map(n, m, seed)
    t = time.perf_counter(); rows = [dij.dijkstra(adj, s)[0] for s in range(n)]; td = (time.perf_counter() - t) * 1000
    t = time.perf_counter(); d = fw.floyd_warshall(n, edges, directed=True)[0]; tf = (time.perf_counter() - t) * 1000
    assert all(rows[i].get(j, float("inf")) == d[i][j] for i in range(n) for j in range(n))
    return {"Dijkstra from every place": round(td, 1), "Floyd-Warshall": round(tf, 1)}


def bidirectional(adj: dict, start, goal, naive: bool = False) -> tuple[float, int, object]:
    """Dijkstra from both ends at once on a two-way map (Section 7.5), alternating one settle from each side.
    mu is the best start-to-goal length seen on any road joining the two searches. Correct rule: stop when the two
    smallest heap keys add up to at least mu. naive=True stops instead at the first place settled by both sides and
    answers through it, which can be wrong. Returns (minutes, places settled in total, meeting place)."""
    if start == goal:
        return 0, 1, start
    dist = ({start: 0}, {goal: 0})
    heaps, done = ([(0, start)], [(0, goal)]), (set(), set())
    mu, meet, settled, side = float("inf"), None, 0, 0
    while heaps[0] and heaps[1]:
        if not naive and heaps[0][0][0] + heaps[1][0][0] >= mu:
            return mu, settled, meet
        d, v = heapq.heappop(heaps[side])
        if v in done[side]:
            continue
        done[side].add(v)
        settled += 1
        if naive and v in done[1 - side]:
            return dist[0][v] + dist[1][v], settled, v
        for w, m in adj[v].items():
            if d + m < dist[side].get(w, float("inf")):
                dist[side][w] = d + m
                heapq.heappush(heaps[side], (d + m, w))
            if w in dist[1 - side] and d + m + dist[1 - side][w] < mu:
                mu, meet = d + m + dist[1 - side][w], w
        side = 1 - side
    return mu, settled, meet


def dijkstra_to_goal(adj: dict, start, goal) -> tuple[float, int]:
    """Plain Dijkstra that stops when the goal is settled. Returns (minutes, places settled)."""
    dist, heap, done = {start: 0}, [(0, start)], set()
    while heap:
        d, v = heapq.heappop(heap)
        if v in done:
            continue
        done.add(v)
        if v == goal:
            return d, len(done)
        for w, m in adj[v].items():
            if d + m < dist.get(w, float("inf")):
                dist[w] = d + m
                heapq.heappush(heap, (d + m, w))
    return float("inf"), len(done)


# Figure 7.2: the first place settled by both searches (U) is not on the shortest route S, A, B, T.
TRICK = {"S": {"A": 3, "U": 5}, "A": {"S": 3, "B": 3}, "B": {"A": 3, "T": 3}, "U": {"S": 5, "T": 5},
         "T": {"B": 3, "U": 5}}


def one_vs_two_ends(n: int, m: int, trials: int = 20, seed: int = 1, grid: int = 0) -> tuple[float, float]:
    """Average places settled, one end against both ends, on a random map (or a grid x grid square grid)."""
    if grid:
        adj = {(r, c): {} for r in range(grid) for c in range(grid)}
        for (r, c) in adj:
            for q in ((r + 1, c), (r, c + 1)):
                if q in adj:
                    adj[(r, c)][q] = adj[q][(r, c)] = 1 + (r * 7 + c * 3) % 5
        nodes = list(adj)
    else:
        adj, _ = random_map(n, m, seed)
        nodes = list(adj)
    rng = random.Random(seed)
    one = two = 0
    for _ in range(trials):
        s, t = rng.choice(nodes), rng.choice(nodes)
        a, n1 = dijkstra_to_goal(adj, s, t)
        b, n2, _ = bidirectional(adj, s, t)
        assert a == b
        one, two = one + n1, two + n2
    return round(one / trials), round(two / trials)


def inflated_guess(factors=(1, 2, 5)) -> list:
    """Challenge 2: A* on Chapter 6's grid with a wall facing the goal, the grid distance multiplied by k.
    Returns (k, minutes, squares expanded) for each k."""
    g = ast.grid_graph(40, ast.POCKET_WALLS)
    h = ast.grid_distance(ast.POCKET_GOAL)
    out = []
    for k in factors:
        minutes, _, done = ast.a_star(g, ast.POCKET_START, ast.POCKET_GOAL, lambda v, k=k: k * h(v))
        out.append((k, minutes, len(done)))
    return out


if __name__ == "__main__":
    print(town_answers())
    for n in (1000, 4000):
        print(n, one_source(n, 3 * n))
    for n in (100, 200):
        print(n, all_pairs(n, 3 * n))
    print(bidirectional(TRICK, "S", "T"), bidirectional(TRICK, "S", "T", naive=True))
    print(one_vs_two_ends(10000, 30000), one_vs_two_ends(0, 0, grid=100))
    print(inflated_guess())
