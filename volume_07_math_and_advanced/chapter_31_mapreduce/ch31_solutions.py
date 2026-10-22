"""Volume 7, Chapter 31 - model solution to the design Thinking Problem: mean and spread per branch in one round.

Run:  python3 ch31_solutions.py
"""

from __future__ import annotations

from ch31_examples import LOANS, map_reduce_counted


def add_triples(key, triples: list) -> tuple:
    """Combiner and reducer input: add (count, sum, sum of squares) triples. Associative and commutative."""
    return tuple(sum(t[i] for t in triples) for i in range(3))


def branch_stats(records: list, machines: int = 3) -> tuple[dict, int]:
    """One MapReduce round: map (branch, x) to (branch, (1, x, x*x)), combine by adding triples on each machine, and
    reduce to (count, mean, variance). Returns ({branch: (count, mean, variance)}, pairs shuffled)."""
    def reducer(key, triples):
        n, s, q = add_triples(key, triples)
        mean = s / n
        return n, mean, q / n - mean * mean
    return map_reduce_counted(records, lambda r: [(r[0], (1, r[1], r[1] * r[1]))], reducer, machines,
                              combiner=add_triples)


if __name__ == "__main__":
    print(branch_stats(LOANS))
    print(branch_stats(LOANS * 1000, machines=10))
