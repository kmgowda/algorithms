"""Volume 15, Chapter 2 - Solutions to the exercises."""

from __future__ import annotations

import itertools


def check_hamiltonian_cycle(adj: dict[int, set[int]], cycle: list[int]) -> bool:
    """Exercise 1: verify a Hamiltonian cycle certificate - every vertex once, consecutive vertices adjacent."""
    return sorted(cycle) == sorted(adj) and all(cycle[i] in adj[cycle[i - 1]] for i in range(len(cycle)))


def two_sat(clauses: list[tuple[int, int]], n_vars: int) -> dict[int, bool] | None:
    """Exercise 2: 2-SAT (two literals per clause) IS in P. A clause (a or b) means 'if not a then b' and
    'if not b then a'. Pick an unset variable, try it true and follow every forced consequence; on a
    contradiction try false instead; if both fail, no assignment exists. O(n x clauses)."""
    implies: dict[int, list[int]] = {}
    for a, b in clauses:
        implies.setdefault(-a, []).append(b)
        implies.setdefault(-b, []).append(a)
    value: dict[int, bool] = {}

    def propagate(lit: int) -> dict[int, bool] | None:
        forced, stack = {abs(lit): lit > 0}, [lit]
        while stack:
            for nxt in implies.get(stack.pop(), []):
                var, want = abs(nxt), nxt > 0
                current = value.get(var, forced.get(var))
                if current is None:
                    forced[var] = want
                    stack.append(nxt)
                elif current != want:
                    return None                      # contradiction
        return forced

    for x in range(1, n_vars + 1):
        if x not in value:
            forced = propagate(x) or propagate(-x)
            if forced is None:
                return None
            value.update(forced)
    return value


def classify(problem: str) -> str:
    """Exercise 3: known classification of some famous problems."""
    return {
        "sorting": "P",
        "shortest path": "P",
        "2-SAT": "P",
        "3-SAT": "NP-complete",
        "subset sum": "NP-complete",
        "travelling salesperson (decision)": "NP-complete",
        "graph 3-colouring": "NP-complete",
        "factoring": "in NP, not known to be NP-complete",
    }[problem]


if __name__ == "__main__":
    print(check_hamiltonian_cycle({0: {1, 3}, 1: {0, 2}, 2: {1, 3}, 3: {2, 0}}, [0, 1, 2, 3]),
          two_sat([(1, 2), (-1, 2), (-2, 3)], 3), classify("factoring"))
