"""Volume 16, Chapter 1 - Solutions to the exercises."""

from __future__ import annotations

from ch01_examples import RUBRIC, feasible_complexity, interview_score


def weakest_area(ratings: dict[str, int]) -> str:
    """Exercise 1: the area whose improvement raises the score most - lowest rating, ties by highest weight."""
    return min(RUBRIC, key=lambda area: (ratings.get(area, 1), -RUBRIC[area]))


def score_if_improved(ratings: dict[str, int], area: str) -> float:
    """Exercise 2: the new score after raising one area by a level (max 4)."""
    better = dict(ratings)
    better[area] = min(4, better.get(area, 1) + 1)
    return interview_score(better)


def best_feasible(n: int) -> str:
    """Exercise 3: the slowest complexity that still fits - the 'budget' to aim for."""
    return feasible_complexity(n)[-1]


if __name__ == "__main__":
    r = {"problem solving": 4, "coding": 3, "communication": 4, "testing": 2, "complexity analysis": 3}
    print(weakest_area(r), score_if_improved(r, "testing"), best_feasible(3000))
