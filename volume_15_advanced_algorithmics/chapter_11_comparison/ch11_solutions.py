"""Volume 15, Chapter 11 - Solutions to the exercises."""

from __future__ import annotations

import random

from ch11_examples import Point, choose_approach, nearest_neighbour, tour_length, two_opt


def best_start_nearest_neighbour(points: list[Point]) -> list[int]:
    """Exercise 1: run nearest neighbour from every start city and keep the shortest tour."""
    return min((nearest_neighbour(points, s) for s in range(len(points))), key=lambda t: tour_length(points, t))


def gap_percent(found: float, optimal: float) -> float:
    """Exercise 2: how far a solution is above optimal, in percent."""
    return 100 * (found - optimal) / optimal


def pick_approaches() -> dict[str, str]:
    """Exercise 3: choose an approach for each job."""
    return {
        "route for 8 delivery stops": choose_approach({"small input"}),
        "network design with a contractual 2x cost bound": choose_approach({"need a proven quality bound"}),
        "daily routes for 2,000 vans by 6 a.m.": choose_approach({"need good answers fast, no proof needed"}),
        "distinct visitors across a billion clicks": choose_approach({"huge data or tight time"}),
    }


if __name__ == "__main__":
    rng = random.Random(0)
    pts = [(rng.random(), rng.random()) for _ in range(20)]
    print(round(tour_length(pts, best_start_nearest_neighbour(pts)), 3), round(tour_length(pts, two_opt(pts, nearest_neighbour(pts))), 3),
          gap_percent(110, 100), pick_approaches()["route for 8 delivery stops"])
