"""Volume 12, Chapter 13 - The Big Comparison: Greedy vs. Divide-and-Conquer vs. Backtracking vs. Dynamic Programming.

One problem - choosing non-overlapping paid jobs - solved four ways.

Run:  python3 ch13_examples.py
"""

from __future__ import annotations

import bisect
import random
import timeit

Job = tuple[int, int, int]           # (start, end, pay)


def greedy_earliest_end(jobs: list[Job]) -> int:
    """Greedy: earliest finish first (optimal for COUNTING jobs, V10-C4) - but pay is ignored, so it can lose money."""
    total, last = 0, -1
    for s, e, p in sorted(jobs, key=lambda j: j[1]):
        if s >= last:
            total += p
            last = e
    return total


def greedy_best_pay(jobs: list[Job]) -> int:
    """Greedy: highest pay first, skipping clashes - also can be wrong."""
    taken: list[Job] = []
    for job in sorted(jobs, key=lambda j: -j[2]):
        if all(job[1] <= t[0] or job[0] >= t[1] for t in taken):
            taken.append(job)
    return sum(p for _, _, p in taken)


def backtracking(jobs: list[Job]) -> int:
    """Backtracking (V11): include or exclude each job, pruning clashes. Exponential."""
    jobs = sorted(jobs)
    best = 0

    def go(i: int, last_end: int, total: int) -> None:
        nonlocal best
        if i == len(jobs):
            best = max(best, total)
            return
        s, e, p = jobs[i]
        if s >= last_end:
            go(i + 1, e, total + p)
        go(i + 1, last_end, total)

    go(0, -1, 0)
    return best


def dynamic_programming(jobs: list[Job]) -> int:
    """DP (weighted interval scheduling, LeetCode 1235): sort by end; best[i] = max(skip job i, take it + best of the
    last job ending before it starts). Binary search finds that job. O(n log n)."""
    jobs = sorted(jobs, key=lambda j: j[1])
    ends = [e for _, e, _ in jobs]
    best = [0] * (len(jobs) + 1)
    for i, (s, e, p) in enumerate(jobs, 1):
        k = bisect.bisect_right(ends, s, 0, i - 1)          # jobs[0..k-1] end by time s
        best[i] = max(best[i - 1], best[k] + p)
    return best[-1]


def divide_and_conquer_note() -> str:
    """Divide-and-conquer doesn't fit: splitting the timeline creates parts that interact at the boundary."""
    return "subproblems are not independent - a job can cross the split"


def random_jobs(n: int, seed: int = 0) -> list[Job]:
    rng = random.Random(seed)
    out = []
    for _ in range(n):
        s = rng.randint(0, 100)
        out.append((s, s + rng.randint(1, 20), rng.randint(1, 50)))
    return out


def race(n: int) -> dict[str, float]:
    jobs = random_jobs(n)
    return {name: min(timeit.repeat(lambda f=f: f(jobs), number=1, repeat=3))
            for name, f in [("greedy", greedy_earliest_end), ("backtracking", backtracking),
                            ("dynamic programming", dynamic_programming)]}


def choose_paradigm(features: set[str]) -> str:
    """The full decision guide for Volumes 10-12."""
    if "a provably safe local choice" in features:
        return "greedy"
    if "independent subproblems combined at the end" in features:
        return "divide and conquer"
    if "overlapping subproblems with a small state" in features:
        return "dynamic programming"
    if "constraints checkable on partial solutions, no small state" in features:
        return "backtracking"
    if "optimization with a good bound, no small state" in features:
        return "branch-and-bound"
    return "brute-force baseline, then look for structure"


if __name__ == "__main__":
    jobs = [(1, 6, 40), (2, 3, 10), (4, 9, 80), (7, 10, 60)]        # (start, end, pay) of freelance jobs
    print("greedy by end:", greedy_earliest_end(jobs), "| greedy by pay:", greedy_best_pay(jobs),
          "| backtracking:", backtracking(jobs), "| DP:", dynamic_programming(jobs))
    print({k: f"{v * 1000:.2f} ms" for k, v in race(26).items()})
    print(divide_and_conquer_note())
