"""Volume 7, Chapter 21 - P, NP, and Reductions: easy to check, hard to find, and problems that turn into each other.

Run:  python3 ch21_examples.py
"""

from __future__ import annotations

import itertools

PRICES = [12, 7, 15, 9, 4, 11, 6, 13, 8, 5]           # book prices; can some of them total exactly the voucher?


def check_subset(prices: list, chosen: list, target: int) -> bool:
    """Checking a proposed answer (a certificate) is fast: add it up."""
    return len(set(chosen)) == len(chosen) and all(0 <= i < len(prices) for i in chosen) and sum(prices[i] for i in chosen) == target


def find_subset(prices: list, target: int) -> tuple[list | None, int]:
    """Finding one by trying subsets: up to 2^n of them. Returns (indices or None, subsets tried)."""
    tried = 0
    for k in range(len(prices) + 1):
        for combo in itertools.combinations(range(len(prices)), k):
            tried += 1
            if sum(prices[i] for i in combo) == target:
                return list(combo), tried
    return None, tried


# Reduction: "is there an independent set of size k in G?" becomes "is there a clique of size k in the complement of G?"
def complement(vertices: list, edges: set) -> set:
    return {(a, b) for a, b in itertools.combinations(vertices, 2) if (a, b) not in edges and (b, a) not in edges}


def has_clique(vertices: list, edges: set, k: int) -> list | None:
    for group in itertools.combinations(vertices, k):
        if all((a, b) in edges or (b, a) in edges for a, b in itertools.combinations(group, 2)):
            return list(group)
    return None


def has_independent_set(vertices: list, edges: set, k: int) -> list | None:
    return has_clique(vertices, complement(vertices, edges), k)       # the whole reduction is one line


TOWN = ["Library", "School", "Park", "Market", "Station", "Museum", "Hospital", "Harbour"]
ROADS = {("Library", "School"), ("Library", "Park"), ("School", "Market"), ("Park", "Market"), ("School", "Station"),
         ("Market", "Station"), ("Market", "Museum"), ("Park", "Hospital"), ("Hospital", "Museum"), ("Station", "Harbour"),
         ("Museum", "Harbour"), ("Station", "Museum")}

# ---------------------------------------------------------------- decision versus optimisation

def largest_independent_set(vertices: list, edges: set) -> tuple[int, int]:
    """Solve the optimisation problem with the yes/no version as a black box: binary search on k.
    Returns (largest k with a 'yes', yes/no questions asked)."""
    lo, hi, asked = 0, len(vertices), 0
    while lo < hi:
        mid = (lo + hi + 1) // 2
        asked += 1
        if has_independent_set(vertices, edges, mid) is not None:
            lo = mid
        else:
            hi = mid - 1
    return lo, asked


# ---------------------------------------------------------------- the Cook-Levin idea: circuits become clauses

# A circuit is a list of gates; each gate is (name, kind, inputs) with kind "in", "not", "and", "or".
# The last gate is the output. Figure 21.4 shows the gate rules as clauses.

def evaluate(circuit: list, inputs: dict) -> bool:
    val = {}
    for name, kind, args in circuit:
        if kind == "in":
            val[name] = inputs[name]
        elif kind == "not":
            val[name] = not val[args[0]]
        elif kind == "and":
            val[name] = all(val[a] for a in args)
        else:
            val[name] = any(val[a] for a in args)
    return val[circuit[-1][0]]


def circuit_satisfiable(circuit: list) -> bool:
    ins = [n for n, k, _ in circuit if k == "in"]
    return any(evaluate(circuit, dict(zip(ins, bits))) for bits in itertools.product([False, True], repeat=len(ins)))


def circuit_to_cnf(circuit: list) -> list:
    """Tseitin's translation: one variable per wire, a few clauses per gate saying "this wire equals its gate's
    output", and one clause saying "the output is true". Clauses are lists of (variable, wanted value)."""
    clauses = []
    for name, kind, args in circuit:
        if kind == "not":
            a = args[0]
            clauses += [[(name, True), (a, True)], [(name, False), (a, False)]]
        elif kind == "and":
            clauses += [[(name, False), (a, True)] for a in args]
            clauses.append([(name, True)] + [(a, False) for a in args])
        elif kind == "or":
            clauses += [[(name, True), (a, False)] for a in args]
            clauses.append([(name, False)] + [(a, True) for a in args])
    clauses.append([(circuit[-1][0], True)])
    return clauses


def cnf_satisfiable(clauses: list) -> tuple[bool, int]:
    """Brute force over every assignment. Returns (satisfiable, assignments tried)."""
    names = sorted({v for c in clauses for v, _ in c})
    tried = 0
    for bits in itertools.product([False, True], repeat=len(names)):
        tried += 1
        val = dict(zip(names, bits))
        if all(any(val[v] == want for v, want in c) for c in clauses):
            return True, tried
    return False, tried


# "Is some subset of prices 4, 7, 9 worth exactly 13?" as a circuit: choose bits x1, x2, x3 and check the sum.
# (A full verifier circuit adds the chosen prices with adder gates; this small one lists the passing choices.)
VOUCHER_CIRCUIT = [("x1", "in", ()), ("x2", "in", ()), ("x3", "in", ()), ("n2", "not", ("x2",)),
                   ("ok", "and", ("x1", "n2", "x3"))]                   # 4 + 9 = 13: x1 and x3, not x2


def random_circuit(rng, inputs: int, gates: int) -> list:
    c = [(f"x{i}", "in", ()) for i in range(inputs)]
    for g in range(gates):
        kind = rng.choice(["not", "and", "or"])
        names = [n for n, _, _ in c]
        if len(names) < 2:
            kind = "not"
        args = (rng.choice(names),) if kind == "not" else tuple(rng.sample(names, 2))
        c.append((f"g{g}", kind, args))
    return c


if __name__ == "__main__":
    print(check_subset(PRICES, [0, 2, 4], 31), find_subset(PRICES, 31), find_subset(PRICES, 200), 2 ** len(PRICES))
    print(has_independent_set(TOWN, ROADS, 3), has_independent_set(TOWN, ROADS, 4), has_independent_set(TOWN, ROADS, 5))
    print(largest_independent_set(TOWN, ROADS), len(complement(TOWN, ROADS)))
    cnf = circuit_to_cnf(VOUCHER_CIRCUIT)
    print(len(cnf), cnf, cnf_satisfiable(cnf), circuit_satisfiable(VOUCHER_CIRCUIT))
