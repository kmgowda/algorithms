"""Volume 7, Chapter 22 - A Tour of NP-Complete Problems: five famous problems, each with a checker and a brute-force search.

Run:  python3 ch22_examples.py
"""

from __future__ import annotations

import itertools

TOWN = ["Library", "School", "Park", "Market", "Station", "Museum", "Hospital", "Harbour"]
ROADS = [("Library", "School"), ("Library", "Park"), ("School", "Market"), ("Park", "Market"), ("School", "Station"),
         ("Market", "Station"), ("Market", "Museum"), ("Park", "Hospital"), ("Hospital", "Museum"), ("Station", "Harbour"),
         ("Museum", "Harbour"), ("Station", "Museum")]


def satisfiable(clauses: list, n_vars: int) -> tuple[dict | None, int]:
    """Satisfiability: clauses are lists of +v / -v; try every true/false setting (Figure 22.1)."""
    tried = 0
    for bits in itertools.product([False, True], repeat=n_vars):
        tried += 1
        if all(any(bits[abs(l) - 1] == (l > 0) for l in c) for c in clauses):
            return {v + 1: bits[v] for v in range(n_vars)}, tried
    return None, tried


def colouring(vertices: list, edges: list, k: int) -> tuple[dict | None, int]:
    tried = 0
    for cols in itertools.product(range(k), repeat=len(vertices)):
        tried += 1
        c = dict(zip(vertices, cols))
        if all(c[a] != c[b] for a, b in edges):
            return c, tried
    return None, tried


def vertex_cover(vertices: list, edges: list, k: int) -> list | None:
    for group in itertools.combinations(vertices, k):
        if all(a in group or b in group for a, b in edges):
            return list(group)
    return None


def bin_packing(sizes: list, capacity: int, bins: int) -> list | None:
    """Can the boxes fit in this many bins? Try every assignment."""
    for assign in itertools.product(range(bins), repeat=len(sizes)):
        load = [0] * bins
        for s, b in zip(sizes, assign):
            load[b] += s
        if max(load, default=0) <= capacity:
            return list(assign)
    return None


# ---------------------------------------------------------------- 3-SAT -> independent set (Figure 22.3)

def sat_to_independent_set(clauses: list) -> tuple[list, list, int]:
    """One triangle per clause (a vertex per literal), plus an edge between every pair of opposite literals.
    The formula is satisfiable exactly when the graph has an independent set of size m = number of clauses.
    Vertices are (clause index, literal). Returns (vertices, edges, m)."""
    vertices = [(i, lit) for i, c in enumerate(clauses) for lit in c]
    edges = []
    for i, c in enumerate(clauses):
        for a, b in itertools.combinations(c, 2):
            edges.append(((i, a), (i, b)))
    for (i, a), (j, b) in itertools.combinations(vertices, 2):
        if i != j and a == -b:
            edges.append(((i, a), (j, b)))
    return vertices, edges, len(clauses)


def independent_set(vertices: list, edges: list, k: int) -> list | None:
    adj = {v: set() for v in vertices}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    for group in itertools.combinations(vertices, k):
        if all(b not in adj[a] for a, b in itertools.combinations(group, 2)):
            return list(group)
    return None


def assignment_from_set(chosen: list, n_vars: int) -> dict:
    """Read a satisfying setting off an independent set: chosen literals are true; others may be anything (false)."""
    val = {v: False for v in range(1, n_vars + 1)}
    for _, lit in chosen:
        val[abs(lit)] = lit > 0
    return val


# ---------------------------------------------------------------- vertex cover and clique, by complements

def cover_from_independent(vertices: list, chosen: list) -> list:
    return [v for v in vertices if v not in chosen]


def complement_edges(vertices: list, edges: list) -> list:
    have = {frozenset(e) for e in edges}
    return [(a, b) for a, b in itertools.combinations(vertices, 2) if frozenset((a, b)) not in have]


# ---------------------------------------------------------------- 3-SAT -> 3-colouring (Figure 22.4)

def sat_to_colouring(clauses: list, n_vars: int) -> tuple[list, list]:
    """The palette triangle TRUE, FALSE, BASE; for each variable a pair x, not-x joined to each other and to BASE;
    for each clause (a or b or c) an OR gadget of 6 vertices whose output is joined to FALSE and BASE.
    The graph is 3-colourable exactly when the formula is satisfiable."""
    V = ["T", "F", "B"]
    E = [("T", "F"), ("F", "B"), ("B", "T")]
    lit = lambda l: f"x{l}" if l > 0 else f"~x{-l}"
    for v in range(1, n_vars + 1):
        V += [f"x{v}", f"~x{v}"]
        E += [(f"x{v}", f"~x{v}"), (f"x{v}", "B"), (f"~x{v}", "B")]
    for i, (a, b, c) in enumerate(clauses):
        p, q, r, s_, o1, o2 = (f"c{i}{t}" for t in "pqrsuv")
        V += [p, q, r, s_, o1, o2]
        # first OR of a and b: p, q are joined to a and b, and to each other; r is joined to p and q (r = a or b)
        E += [(lit(a), p), (lit(b), q), (p, q), (p, r), (q, r)]
        # second OR of r and c: s, o1 joined to r and c and each other; o2 = r or c is the output
        E += [(r, s_), (lit(c), o1), (s_, o1), (s_, o2), (o1, o2)]
        E += [(o2, "F"), (o2, "B")]                       # the output must take the colour TRUE
    return V, E


def three_colourable(vertices: list, edges: list) -> bool:
    """Backtracking 3-colouring (exact, fine for small graphs)."""
    adj = {v: set() for v in vertices}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    order = sorted(vertices, key=lambda v: -len(adj[v]))
    col = {}

    def go(i):
        if i == len(order):
            return True
        v = order[i]
        for c in range(3):
            if all(col.get(u) != c for u in adj[v]):
                col[v] = c
                if go(i + 1):
                    return True
                del col[v]
        return False
    return go(0)


# ---------------------------------------------------------------- Hamiltonian cycle -> travelling salesperson

def hamiltonian_cycle(vertices: list, edges: list) -> list | None:
    have = {frozenset(e) for e in edges}
    if len(vertices) < 3:
        return None
    first = vertices[0]
    for rest in itertools.permutations(vertices[1:]):
        tour = [first, *rest]
        if all(frozenset((tour[i], tour[(i + 1) % len(tour)])) in have for i in range(len(tour))):
            return tour
    return None


def ham_to_tsp(vertices: list, edges: list) -> tuple[dict, int]:
    """Distances 1 for roads, 2 for non-roads; a Hamiltonian cycle exists exactly when a round of length n exists."""
    have = {frozenset(e) for e in edges}
    dist = {frozenset((a, b)): (1 if frozenset((a, b)) in have else 2) for a, b in itertools.combinations(vertices, 2)}
    return dist, len(vertices)


def shortest_round(vertices: list, dist: dict) -> tuple[int, list]:
    first = vertices[0]
    best = None
    for rest in itertools.permutations(vertices[1:]):
        tour = [first, *rest]
        length = sum(dist[frozenset((tour[i], tour[(i + 1) % len(tour)]))] for i in range(len(tour)))
        if best is None or length < best[0]:
            best = (length, tour)
    return best


# ---------------------------------------------------------------- subset sum: pseudo-polynomial

def subset_sum_table(prices: list, target: int) -> tuple[bool, int]:
    """The knapsack-style table (Volume 6): reachable sums, one row per price. Returns (possible?, cells filled)."""
    reach = [True] + [False] * target
    cells = 0
    for p in prices:
        for t in range(target, p - 1, -1):
            cells += 1
            if reach[t - p]:
                reach[t] = True
    return reach[target], cells


EXAMPLE = [[1, 2, 3], [-1, -2, 3], [1, -2, -3]]          # (x1 or x2 or x3) and (not x1 or not x2 or x3) and (x1 or not x2 or not x3)


def vertex_cover_to_ham(n: int, edges: list, k: int) -> dict:
    """Section 22.7: the 12-vertex road gadgets, place chains and k selectors of G' (adjacency sets)."""
    adj = {}

    def link(a, b):
        adj.setdefault(a, set()).add(b)
        adj.setdefault(b, set()).add(a)
    roads_at = {u: [] for u in range(n)}
    for u, v in edges:
        for a, b in ((u, v), (v, u)):
            for i in range(1, 6):
                link((a, b, i), (a, b, i + 1))
        link((u, v, 1), (v, u, 3)); link((u, v, 3), (v, u, 1))
        link((u, v, 4), (v, u, 6)); link((u, v, 6), (v, u, 4))
        roads_at[u].append(v); roads_at[v].append(u)
    for u in range(n):
        for a, b in zip(roads_at[u], roads_at[u][1:]):
            link((u, a, 6), (u, b, 1))
    for s in range(k):
        for u in range(n):
            if roads_at[u]:
                link(("selector", s), (u, roads_at[u][0], 1))
                link(("selector", s), (u, roads_at[u][-1], 6))
    return adj


def has_ham_cycle(adj: dict) -> bool:
    """Backtracking search for a cycle through every vertex (small graphs only)."""
    vertices = list(adj)
    if not vertices:
        return False
    start, seen = vertices[0], {vertices[0]}

    def extend(x, count):
        if count == len(vertices):
            return start in adj[x]
        for y in adj[x]:
            if y not in seen:
                seen.add(y)
                if extend(y, count + 1):
                    return True
                seen.discard(y)
        return False
    return extend(start, 1)


def has_cover(n: int, edges: list, k: int) -> bool:
    """Brute force: is there a vertex cover of at most k places?"""
    return any(all(u in s or v in s for u, v in edges)
               for r in range(k + 1) for s in map(set, itertools.combinations(range(n), r)))


if __name__ == "__main__":
    clauses = [[1, 2], [-1, 3], [-2, -3], [2, 3]]
    print(satisfiable(clauses, 3), satisfiable([[1], [-1]], 1))
    print(colouring(TOWN, ROADS, 2)[0], colouring(TOWN, ROADS, 2)[1], colouring(TOWN, ROADS, 3))
    print(vertex_cover(TOWN, ROADS, 3), vertex_cover(TOWN, ROADS, 4), vertex_cover(TOWN, ROADS, 5))
    print(bin_packing([5, 4, 4, 3, 2, 2], 10, 2), bin_packing([6, 6, 6], 10, 2))
    V, E, m = sat_to_independent_set(EXAMPLE)
    chosen = independent_set(V, E, m)
    print(len(V), len(E), m, chosen, assignment_from_set(chosen, 3), satisfiable(EXAMPLE, 3))
    CV, CE = sat_to_colouring(EXAMPLE, 3)
    print(len(CV), len(CE), three_colourable(CV, CE))
    unsat = [[1, 1, 1], [-1, -1, -1]]
    print(three_colourable(*sat_to_colouring(unsat, 1)), independent_set(*sat_to_independent_set(unsat)[:2], 2))
    dist, n = ham_to_tsp(TOWN, ROADS)
    print(hamiltonian_cycle(TOWN, ROADS), shortest_round(TOWN, dist))
    print(subset_sum_table([12, 7, 15, 9, 4, 11, 6, 13, 8, 5], 31), subset_sum_table([12, 7, 15, 9, 4, 11, 6, 13, 8, 5], 200))
