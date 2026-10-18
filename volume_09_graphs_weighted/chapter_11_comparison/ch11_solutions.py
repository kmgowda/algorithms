"""Volume 9, Chapter 11 - Solutions to the exercises."""

from __future__ import annotations

from ch11_examples import choose


def pick_for_scenarios() -> dict[str, str]:
    """Exercise 1: match real scenarios to algorithms."""
    return {
        "phone navigation to one address": choose("one source and one target with a good estimate"),
        "bank checking exchange rates for profit loops": choose("one source, negative edges or negative-cycle check"),
        "distance chart for 50 cities": choose("all pairs, small or dense graph"),
        "fibre network joining 10,000 homes from a list of possible links": choose("cheapest network, sparse edge list"),
        "evacuation capacity of a road network": choose("most throughput"),
        "a project's earliest finish time": choose("one source, DAG"),
    }


def mst_vs_shortest_path_tree() -> dict[str, float]:
    """Exercise 2: on a triangle, the MST and Dijkstra's tree differ.
    Edges: A-B 2, B-C 2, A-C 3. MST = A-B + B-C = 4 total; shortest-path tree from A uses A-C (3) directly."""
    return {"MST total": 4.0, "shortest-path tree total": 5.0, "A to C in MST": 4.0, "A to C shortest": 3.0}


if __name__ == "__main__":
    print(pick_for_scenarios())
    print(mst_vs_shortest_path_tree())
