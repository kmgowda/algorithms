"""Volume 15, Chapter 3 - Solutions to the exercises."""

from __future__ import annotations

from ch03_examples import Clause, Graph


def sat_to_3sat(clauses: list[Clause], n_vars: int) -> tuple[list[Clause], int]:
    """Exercise 1: split long clauses (a or b or c or d) into (a or b or y) and (not y or c or d) with fresh
    variables y; pad short clauses by repeating a literal. Satisfiable exactly when the original is."""
    out: list[Clause] = []
    nxt = n_vars
    for cl in clauses:
        lits = list(cl)
        while len(lits) > 3:
            nxt += 1
            out.append((lits[0], lits[1], nxt))
            lits = [-nxt] + lits[2:]
        while len(lits) < 3:
            lits.append(lits[0])
        out.append(tuple(lits))
    return out, nxt


def subset_sum_to_partition(values: list[int], target: int) -> list[int]:
    """Exercise 2: add two items so that an equal split exists exactly when some subset hits target.
    With total S, add (S + target) and (2S - target): each half must then sum to 2S."""
    s = sum(values)
    return values + [s + target, 2 * s - target]


def hamiltonian_path_to_cycle(graph: Graph) -> Graph:
    """Exercise 3: add one new vertex joined to everyone - a Hamiltonian path in G becomes a cycle through it."""
    hub = max(graph, default=-1) + 1
    g = {v: set(n) | {hub} for v, n in graph.items()}
    g[hub] = set(graph)
    return g


if __name__ == "__main__":
    print(sat_to_3sat([(1, 2, 3, 4), (-1,)], 4), subset_sum_to_partition([3, 1, 4], 5),
          hamiltonian_path_to_cycle({0: {1}, 1: {0, 2}, 2: {1}}))
