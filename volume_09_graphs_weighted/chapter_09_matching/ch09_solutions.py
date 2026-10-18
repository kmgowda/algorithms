"""Volume 9, Chapter 9 - Solutions to the exercises."""

from __future__ import annotations

import itertools
from collections import deque
from typing import Hashable

from ch09_examples import max_bipartite_matching


def matching_via_flow(likes: dict[Hashable, list[Hashable]]) -> int:
    """Exercise 1: the same answer through max flow - source -> people -> jobs -> sink, all capacities 1."""
    cap: dict[Hashable, dict[Hashable, int]] = {}

    def add(u, v):
        cap.setdefault(u, {}).setdefault(v, 0)
        cap.setdefault(v, {}).setdefault(u, 0)
        cap[u][v] += 1
    for p, jobs in likes.items():
        add("SRC", ("p", p))
        for j in jobs:
            add(("p", p), ("j", j))
    for j in {j for jobs in likes.values() for j in jobs}:
        add(("j", j), "SNK")                     # each job can be filled once
    total = 0
    while True:
        parent = {"SRC": None}
        q = deque(["SRC"])
        while q and "SNK" not in parent:
            u = q.popleft()
            for v, c in cap.get(u, {}).items():
                if c > 0 and v not in parent:
                    parent[v] = u
                    q.append(v)
        if "SNK" not in parent:
            return total
        v = "SNK"
        while parent[v] is not None:
            u = parent[v]
            cap[u][v] -= 1
            cap[v][u] += 1
            v = u
        total += 1


def brute_force_matching(likes: dict[Hashable, list[Hashable]]) -> int:
    """Exercise 2: largest set of (person, job) pairs with no repeats, by trying all subsets (tiny inputs)."""
    pairs = [(p, j) for p, jobs in likes.items() for j in jobs]
    for k in range(len(likes), -1, -1):
        for combo in itertools.combinations(pairs, k):
            if len({p for p, _ in combo}) == k and len({j for _, j in combo}) == k:
                return k
    return 0


def is_perfect(likes: dict[Hashable, list[Hashable]]) -> bool:
    """Exercise 3: can EVERY person get a job?"""
    return len(max_bipartite_matching(likes)) == len(likes)


if __name__ == "__main__":
    likes = {"Ana": ["cook", "driver"], "Ben": ["cook"], "Cy": ["driver", "guide"], "Dev": ["guide"]}
    print(matching_via_flow(likes), brute_force_matching(likes), is_perfect(likes))
