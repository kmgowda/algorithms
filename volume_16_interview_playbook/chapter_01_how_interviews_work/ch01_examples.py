"""Volume 16, Chapter 1 - How Coding Interviews Work.

Run:  python3 ch01_examples.py
"""

from __future__ import annotations

import math

RUBRIC = {
    "problem solving": 0.30,
    "coding": 0.25,
    "communication": 0.20,
    "testing": 0.15,
    "complexity analysis": 0.10,
}


def interview_score(ratings: dict[str, int]) -> float:
    """Weighted score from 1-4 ratings per area (a typical structured rubric). Missing areas count as 1."""
    return round(sum(weight * ratings.get(area, 1) for area, weight in RUBRIC.items()), 2)


def hiring_signal(score: float) -> str:
    """Map a weighted score to the four-level signal most companies use."""
    if score >= 3.5:
        return "strong hire"
    if score >= 2.75:
        return "hire"
    if score >= 2.0:
        return "no hire"
    return "strong no hire"


def time_plan(total_minutes: int) -> dict[str, int]:
    """Split a coding round into phases (proportions from Chapter 2's framework)."""
    shares = {"clarify": 0.10, "plan": 0.20, "code": 0.40, "test": 0.20, "discuss": 0.10}
    plan = {phase: int(total_minutes * s) for phase, s in shares.items()}
    plan["code"] += total_minutes - sum(plan.values())          # rounding leftovers go to coding
    return plan


def feasible_complexity(n: int, ops_per_second: float = 1e7, seconds: float = 1.0) -> list[str]:
    """Which complexities fit the limit for input size n (Python does roughly 10^7 simple steps per second)."""
    budget = ops_per_second * seconds
    candidates = {
        "O(log n)": math.log2(max(n, 2)),
        "O(n)": n,
        "O(n log n)": n * math.log2(max(n, 2)),
        "O(n^2)": n ** 2,
        "O(n^3)": n ** 3,
        "O(2^n)": 2.0 ** n if n < 1000 else math.inf,
        "O(n!)": math.factorial(n) if n < 25 else math.inf,
    }
    return [name for name, cost in candidates.items() if cost <= budget]


if __name__ == "__main__":
    candidate = {"problem solving": 4, "coding": 3, "communication": 4, "testing": 2, "complexity analysis": 3}
    s = interview_score(candidate)
    print(s, hiring_signal(s))
    print(time_plan(45))
    for n in (20, 3000, 10 ** 5, 10 ** 7):
        print(n, feasible_complexity(n))
