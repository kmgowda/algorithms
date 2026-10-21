"""Volume 4, Chapter 7 - Every Shortest-Path Algorithm on One Map.

Runs the methods of Chapters 1-6 on the same inputs and compares answers, work, and time.
Run:  python3 ch07_examples.py
"""

from __future__ import annotations

import importlib.util
import os
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
    """Library-to-Harbour minutes from every method (Figure 7.1)."""
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
    """Milliseconds for one start: Dijkstra against Bellman-Ford (Figure 7.3)."""
    adj, edges = random_map(n, m, seed)
    t = time.perf_counter(); a = dij.dijkstra(adj, 0)[0]; td = (time.perf_counter() - t) * 1000
    t = time.perf_counter(); b = bf.bellman_ford(list(range(n)), edges, 0)[0]; tb = (time.perf_counter() - t) * 1000
    assert all(a.get(v, float("inf")) == b[v] for v in range(n))
    return {"Dijkstra": round(td, 1), "Bellman-Ford": round(tb, 1)}


def all_pairs(n: int, m: int, seed: int = 1) -> dict:
    """Milliseconds for every pair: Dijkstra from each place against Floyd-Warshall (Figure 7.3)."""
    adj, edges = random_map(n, m, seed)
    t = time.perf_counter(); rows = [dij.dijkstra(adj, s)[0] for s in range(n)]; td = (time.perf_counter() - t) * 1000
    t = time.perf_counter(); d = fw.floyd_warshall(n, edges, directed=True)[0]; tf = (time.perf_counter() - t) * 1000
    assert all(rows[i].get(j, float("inf")) == d[i][j] for i in range(n) for j in range(n))
    return {"Dijkstra from every place": round(td, 1), "Floyd-Warshall": round(tf, 1)}


if __name__ == "__main__":
    print(town_answers())
    for n in (1000, 4000):
        print(n, one_source(n, 3 * n))
    for n in (100, 200):
        print(n, all_pairs(n, 3 * n))
