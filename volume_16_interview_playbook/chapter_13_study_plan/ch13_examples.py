"""Volume 16, Chapter 13 - Your 90-Day Study Plan.

Run:  python3 ch13_examples.py
"""

from __future__ import annotations

PHASES = [
    ("foundations review", 14, ["Big O", "arrays and strings", "hashing", "two pointers", "sliding window"]),
    ("core patterns", 35, ["linked lists", "stacks and queues", "binary search", "trees", "graphs BFS/DFS",
                           "heaps", "intervals and greedy"]),
    ("hard patterns", 28, ["backtracking", "1-D DP", "2-D DP", "union-find and topological sort", "tries",
                           "design questions"]),
    ("interview mode", 13, ["timed mixed sets", "mock interviews", "review weakest topics"]),
]

REVIEW_GAPS = [1, 3, 7, 14, 30]


def build_plan() -> list[tuple[int, str, str]]:
    """Spread each phase's topics evenly over its days. Returns (day, phase, topic) for days 1..90."""
    plan, day = [], 1
    for phase, days, topics in PHASES:
        for k in range(days):
            plan.append((day, phase, topics[k * len(topics) // days]))
            day += 1
    return plan


def review_days(solved_on: int, horizon: int = 90) -> list[int]:
    """Spaced repetition: re-solve a problem 1, 3, 7, 14 and 30 days after first solving it."""
    return [solved_on + g for g in REVIEW_GAPS if solved_on + g <= horizon]


def daily_load(solved: dict[int, int], horizon: int = 90) -> list[int]:
    """How many reviews fall on each day, given {day: problems first solved that day}."""
    load = [0] * (horizon + 1)
    for day, count in solved.items():
        for r in review_days(day, horizon):
            load[r] += count
    return load


def readiness(results: dict[str, list[bool]]) -> dict[str, float]:
    """Per-topic success rate over the latest five attempts - the topics below 0.6 need more work."""
    return {topic: round(sum(r[-5:]) / len(r[-5:]), 2) for topic, r in results.items() if r}


if __name__ == "__main__":
    plan = build_plan()
    print(len(plan), plan[0], plan[14], plan[49], plan[-1])
    print(review_days(10))
    load = daily_load({d: 2 for d in range(1, 78)})
    print("busiest review day:", max(range(len(load)), key=load.__getitem__), max(load))
    print(readiness({"graphs": [True, False, True, True, True], "dp": [False, False, True, False, True, False]}))
