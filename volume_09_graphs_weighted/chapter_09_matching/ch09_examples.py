"""Volume 9, Chapter 9 - Bipartite Matching and Assignment Problems.

Run:  python3 ch09_examples.py
"""

from __future__ import annotations

import itertools
from typing import Hashable


def max_bipartite_matching(likes: dict[Hashable, list[Hashable]]) -> dict[Hashable, Hashable]:
    """Kuhn's augmenting-path algorithm. likes[person] = jobs they can do.
    For each person, look for a free job - or a job whose holder can be moved to another job (an augmenting path).
    O(V * E). Returns job -> person."""
    holder: dict[Hashable, Hashable] = {}

    def try_assign(person: Hashable, visited: set) -> bool:
        for job in likes.get(person, []):
            if job in visited:
                continue
            visited.add(job)
            if job not in holder or try_assign(holder[job], visited):
                holder[job] = person
                return True
        return False

    for person in likes:
        try_assign(person, set())
    return holder


def min_cost_assignment(cost: list[list[float]]) -> tuple[float, list[int]]:
    """Assignment problem: n workers, n tasks, cost[w][t]; give each worker one task at least total cost.
    Exact by trying every permutation (n! - fine for n <= 8). The Hungarian algorithm does it in O(n^3)."""
    n = len(cost)
    best: tuple[float, list[int]] = (float("inf"), [])
    for perm in itertools.permutations(range(n)):
        total = sum(cost[w][perm[w]] for w in range(n))
        if total < best[0]:
            best = (total, list(perm))
    return best


def bitmask_assignment(cost: list[list[float]]) -> float:
    """Faster exact assignment: dp over subsets of tasks already used - O(2^n * n) (Volume 12 explains DP)."""
    n = len(cost)
    dp = [float("inf")] * (1 << n)
    dp[0] = 0.0
    for mask in range(1 << n):
        worker = bin(mask).count("1")                       # tasks used so far = workers already placed
        if worker == n or dp[mask] == float("inf"):
            continue
        for t in range(n):
            if not mask & (1 << t):
                nxt = mask | (1 << t)
                dp[nxt] = min(dp[nxt], dp[mask] + cost[worker][t])
    return dp[(1 << n) - 1]


def school_admissions(prefs: dict[str, list[str]], seats: dict[str, int]) -> dict[str, list[str]]:
    """Industry example: students list acceptable schools; schools have seats. Maximise students placed.
    Split each school into one vertex per seat, then match."""
    likes = {s: [(school, k) for school in schools for k in range(seats[school])] for s, schools in prefs.items()}
    holder = max_bipartite_matching(likes)
    out: dict[str, list[str]] = {school: [] for school in seats}
    for (school, _), student in holder.items():
        out[school].append(student)
    return {k: sorted(v) for k, v in out.items()}


if __name__ == "__main__":
    likes = {"Ana": ["cook", "driver"], "Ben": ["cook"], "Cy": ["driver", "guide"], "Dev": ["guide"]}
    print("matching:", max_bipartite_matching(likes))
    cost = [[9, 2, 7, 8], [6, 4, 3, 7], [5, 8, 1, 8], [7, 6, 9, 4]]
    print("assignment:", min_cost_assignment(cost), "| bitmask:", bitmask_assignment(cost))
    print(school_admissions({"Ria": ["North"], "Sam": ["North", "South"], "Tia": ["North"], "Uma": ["South"]},
                            {"North": 2, "South": 1}))
