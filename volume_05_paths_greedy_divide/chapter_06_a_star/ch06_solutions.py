"""Volume 5, Chapter 6 - Thinking Problems: A* on the parcel state graph with a perfect, consistent guess
(Thinking Problem 2), and the average-speed guess that overestimates (Thinking Problem 3).

Run:  python3 ch06_solutions.py
"""

from __future__ import annotations

import ch06_examples as ex


def parcel_a_star(adj: dict, start, via, goal) -> tuple[float, list | None, int]:
    """Quickest route from start to goal that calls at via, by A* on the states (place, parcel on board?).
    Two Dijkstra runs on reversed roads give the guesses: d(v, via) + d(via, goal) before the parcel is collected,
    d(v, goal) after. Returns (minutes, places along the route, states expanded)."""
    to_via, to_goal = ex.true_remaining(adj, via), ex.true_remaining(adj, goal)
    inf = float("inf")
    states = {}
    for v in adj:
        for got in (False, True):
            states[(v, got)] = {(w, got or w == via): m for w, m in adj[v].items()}

    def h(state):
        v, got = state
        return to_goal.get(v, inf) if got else to_via.get(v, inf) + to_goal.get(via, inf)

    first = (start, start == via)
    if h(first) == inf:
        return inf, None, 0
    minutes, path, expanded = ex.a_star(states, first, (goal, True), h)
    return minutes, (None if path is None else [v for v, _ in path]), len(expanded)


def average_speed_guess(goal):
    """The WRONG sharper guess: straight-line distance times the AVERAGE minutes per map unit of the roads."""
    rates = [w / ex.crow_flies(a, b) for a, b, w in ex.ROADS]
    speed = sum(rates) / len(rates)
    return lambda v: speed * ex.crow_flies(v, goal)


if __name__ == "__main__":
    adj = ex.weighted_adjacency()
    print(parcel_a_star(adj, "Library", "Market", "Harbour"))
    print(ex.a_star(adj, "Library", "Harbour", average_speed_guess("Harbour")))
