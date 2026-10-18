"""Volume 8, Chapter 11 - Solutions to the exercises."""

from __future__ import annotations

from ch11_examples import choose


def pick_for_scenarios() -> dict[str, str]:
    """Exercise 1: match scenarios to techniques."""
    return {
        "fewest train changes between two stations": choose("fewest hops"),
        "install order for software packages": choose("cycles, topological order"),
        "which cables are single points of failure": choose("bridges and cut vertices"),
        "friend groups as a social network grows": choose("connected? as edges keep arriving"),
        "can students be split into two rival teams": choose("two-sided split"),
    }


def frontier_shapes() -> dict[str, str]:
    """Exercise 2: which search keeps less in memory on each shape?"""
    return {"wide, shallow (a star)": "DFS", "long, thin (a chain)": "BFS"}


if __name__ == "__main__":
    print(pick_for_scenarios())
    print(frontier_shapes())
