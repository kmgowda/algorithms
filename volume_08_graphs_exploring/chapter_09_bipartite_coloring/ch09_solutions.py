"""Volume 8, Chapter 9 - Solutions to the exercises."""

from __future__ import annotations

from itertools import product

from ch09_examples import Graph, greedy_coloring, two_color


def possible_bipartition(n: int, dislikes: list[tuple[int, int]]) -> bool:
    """Exercise 1 (LeetCode 886): split people into two groups so no one is with someone they dislike."""
    graph: Graph = {p: [] for p in range(1, n + 1)}
    for a, b in dislikes:
        graph[a].append(b)
        graph[b].append(a)
    return two_color(graph) is not None


def chromatic_number(graph: Graph) -> int:
    """Exercise 2: the true minimum number of colours, by trying every assignment (tiny graphs only)."""
    vertices = list(graph)
    for k in range(1, len(vertices) + 1):
        for assignment in product(range(k), repeat=len(vertices)):
            col = dict(zip(vertices, assignment))
            if all(col[u] != col[v] for u in graph for v in graph[u]):
                return k
    return 0


def bad_greedy_order() -> tuple[int, int]:
    """Exercise 3: a bipartite 'crown' graph where a poor order makes greedy use 4 colours instead of 2."""
    g: Graph = {f"a{i}": [] for i in range(4)} | {f"b{i}": [] for i in range(4)}
    for i in range(4):
        for j in range(4):
            if i != j:
                g[f"a{i}"].append(f"b{j}")
                g[f"b{j}"].append(f"a{i}")
    interleaved = [x for i in range(4) for x in (f"a{i}", f"b{i}")]
    return max(greedy_coloring(g, interleaved).values()) + 1, max(two_color(g).values()) + 1  # type: ignore[union-attr]


def is_valid_coloring(graph: Graph, color: dict) -> bool:
    """Exercise 4: no edge joins two vertices of the same colour."""
    return all(color[u] != color[v] for u in graph for v in graph[u])


if __name__ == "__main__":
    print(possible_bipartition(4, [(1, 2), (1, 3), (2, 4)]), possible_bipartition(3, [(1, 2), (1, 3), (2, 3)]))
    print(chromatic_number({"a": ["b", "c"], "b": ["a", "c"], "c": ["a", "b"]}), bad_greedy_order())
