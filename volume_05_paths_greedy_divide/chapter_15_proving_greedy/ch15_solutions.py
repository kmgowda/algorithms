"""Volume 5, Chapter 15 - Thinking Problems.

Problem 1: shortest job first minimises the total of finishing times (checked against every order).
Problem 2: one-hour jobs with deadlines and rewards: take jobs by reward into the latest free hour (union-find).
Problem 3: least slack first (due - hours) is not optimal for the largest lateness: a three-job counterexample.
"""

from __future__ import annotations

import itertools

from ch15_examples import best_lateness, lateness


def total_finish(order: list) -> int:
    t = total = 0
    for _, hours in order:
        t += hours
        total += t
    return total


def shortest_first(jobs: list) -> list:
    return sorted(jobs, key=lambda j: j[1])


def best_total_finish(jobs: list) -> int:
    return min((total_finish(list(p)) for p in itertools.permutations(jobs)), default=0)


def schedule_rewards(jobs: list) -> tuple[int, dict]:
    """jobs: (name, deadline hour >= 1, reward); each takes one hour, hours 1, 2, ... Returns (reward, hour -> job)."""
    latest = max((d for _, d, _ in jobs), default=0)
    parent = list(range(latest + 1))                 # parent[h]: a free hour at or before h (0 = none)

    def find(h):
        while parent[h] != h:
            parent[h] = parent[parent[h]]
            h = parent[h]
        return h
    total, plan = 0, {}
    for name, deadline, reward in sorted(jobs, key=lambda j: -j[2]):
        h = find(min(deadline, latest))
        if h > 0:
            plan[h], total = name, total + reward
            parent[h] = h - 1                        # hour h is taken: point to the hour before
    return total, plan


def best_rewards(jobs: list) -> int:
    best = 0
    for k in range(len(jobs) + 1):
        for chosen in itertools.combinations(jobs, k):
            ds = sorted(d for _, d, _ in chosen)
            if all(d >= i + 1 for i, d in enumerate(ds)):
                best = max(best, sum(r for *_, r in chosen))
    return best


SLACK_TRAP = [("A", 2, 5), ("B", 5, 7), ("C", 2, 8)]


def least_slack_first(jobs: list) -> list:
    return sorted(jobs, key=lambda j: j[2] - j[1])


if __name__ == "__main__":
    jobs = [("Map", 3), ("Atlas", 1), ("Novel", 4), ("Poems", 2)]
    print(total_finish(shortest_first(jobs)), best_total_finish(jobs))
    print(schedule_rewards([("a", 2, 100), ("b", 1, 19), ("c", 2, 27), ("d", 1, 25), ("e", 3, 15)]))
    print(lateness(least_slack_first(SLACK_TRAP))[0], best_lateness(SLACK_TRAP))
