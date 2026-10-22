"""Volume 4, Chapter 25 - Comparing Graph Explorations: every method of Part II on the same graphs.

Run:  python3 ch25_examples.py
"""

from __future__ import annotations

import importlib.util
import os
import random
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.setrecursionlimit(20_000)


def _load(folder: str, module: str):
    spec = importlib.util.spec_from_file_location(f"v3_{module}", os.path.join(HERE, "..", folder, f"{module}.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


bfs_m = _load("chapter_17_breadth_first_search", "ch17_examples")
dfs_m = _load("chapter_18_depth_first_search", "ch18_examples")
topo_m = _load("chapter_21_cycles_and_topological_order", "ch21_examples")
comp_m = _load("chapter_22_connected_pieces", "ch22_examples")
bip_m = _load("chapter_23_bipartite_graphs", "ch23_examples")
weak_m = _load("chapter_24_bridges_and_cut_vertices", "ch24_examples")

PLACES, ROADS = bfs_m.PLACES, bfs_m.ROADS


def town_answers() -> dict:
    """The question each method answers, asked of the town (Section 25.4)."""
    adj = bfs_m.adjacency()
    dist, parent = bfs_m.bfs(adj, "Library")
    d = dfs_m.dfs(adj, "Library")
    colour, cyc = bip_m.two_colour(bip_m.adjacency(PLACES, ROADS))
    w = weak_m.weak_links(weak_m.adjacency(PLACES, ROADS))
    return {"fewest roads Library to Harbour (BFS)": dist["Harbour"],
            "back roads, so cycles (DFS)": sum(1 for e in d["edges"] if e[2] == "back"),
            "pieces (components)": len(comp_m.components(comp_m.adjacency())),
            "two-colourable (bipartite)": colour is not None,
            "bridges": len(w["bridges"]), "cut places": len(w["cuts"])}


def random_graph(n: int, m: int, seed: int = 1) -> list[tuple]:
    rng = random.Random(seed)
    roads = set()
    while len(roads) < m:
        a, b = rng.randrange(n), rng.randrange(n)
        if a != b:
            roads.add((min(a, b), max(a, b)))
    return sorted(roads)


def timings(n: int = 3000, m: int = 9000, seed: int = 1, repeats: int = 5) -> dict:
    """Milliseconds for each method on the same random graph of n places and m roads, the median of several runs
    (Figure 25.2)."""
    roads = random_graph(n, m, seed)
    places = list(range(n))
    adj = bfs_m.adjacency(places, roads)
    dag = {v: [] for v in places}
    for a, b in roads:                                 # orient every road from smaller to larger: a DAG
        dag[a].append(b)
    out = {}
    for name, fn in (("BFS", lambda: bfs_m.bfs(adj, 0)),
                     ("DFS (recursive)", lambda: dfs_m.dfs(adj, 0)),
                     ("components", lambda: comp_m.components(adj)),
                     ("topological order (Kahn)", lambda: topo_m.kahn(dag)),
                     ("strongly connected (Kosaraju)", lambda: comp_m.strongly_connected(dag)),
                     ("strongly connected (Tarjan)", lambda: comp_m.tarjan_scc(dag)),
                     ("two-colouring", lambda: bip_m.two_colour(adj)),
                     ("bridges and cut places", lambda: weak_m.weak_links(adj)),
                     ("blocks", lambda: weak_m.blocks(adj))):
        runs = []
        for _ in range(repeats):
            t = time.perf_counter()
            fn()
            runs.append((time.perf_counter() - t) * 1e3)
        out[name] = round(sorted(runs)[len(runs) // 2], 1)
    return out


if __name__ == "__main__":
    print(town_answers())
    print(timings())
    print(timings(6000, 18000))
