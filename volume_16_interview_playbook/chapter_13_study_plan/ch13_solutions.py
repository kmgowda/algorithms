"""Volume 16, Chapter 13 - Solutions to the exercises."""

from __future__ import annotations

from ch13_examples import build_plan, readiness


def weak_topics(results: dict[str, list[bool]], threshold: float = 0.6) -> list[str]:
    """Exercise 1: topics whose recent success rate is below the threshold, weakest first."""
    scores = readiness(results)
    return sorted((t for t, s in scores.items() if s < threshold), key=lambda t: (scores[t], t))


def compressed_plan(days: int) -> list[tuple[int, str, str]]:
    """Exercise 2: squeeze the 90-day plan into fewer days by sampling it evenly (same order of topics)."""
    full = build_plan()
    return [(d + 1, *full[d * len(full) // days][1:]) for d in range(days)]


def topics_covered(plan: list[tuple[int, str, str]]) -> set[str]:
    """Exercise 3: which topics a plan touches at least once."""
    return {topic for _, _, topic in plan}


if __name__ == "__main__":
    print(weak_topics({"graphs": [True] * 5, "dp": [False, True, False], "tries": [False]}))
    print(len(compressed_plan(30)), len(topics_covered(compressed_plan(30))), len(topics_covered(build_plan())))
