"""Volume 9, Chapter 5 - Solutions to the exercises."""

from __future__ import annotations

from ch05_examples import INF, floyd_warshall


def transitive_closure(n: int, edges: list[tuple[int, int]]) -> list[list[bool]]:
    """Exercise 1 (Warshall's algorithm): reach[i][j] = can i reach j at all? Same loops with 'or' and 'and'."""
    reach = [[i == j for j in range(n)] for i in range(n)]
    for u, v in edges:
        reach[u][v] = True
    for k in range(n):
        for i in range(n):
            if reach[i][k]:
                for j in range(n):
                    reach[i][j] = reach[i][j] or reach[k][j]
    return reach


def city_with_fewest_reachable(n: int, edges: list[tuple[int, int, int]], threshold: int) -> int:
    """Exercise 2 (LeetCode 1334): the city with the fewest neighbours within the threshold (ties -> larger id)."""
    two_way = edges + [(b, a, w) for a, b, w in edges]
    dist, _ = floyd_warshall(n, two_way)
    counts = [sum(1 for j in range(n) if j != i and dist[i][j] <= threshold) for i in range(n)]
    return min(range(n), key=lambda i: (counts[i], -i))


def has_negative_cycle(n: int, edges: list[tuple[int, int, float]]) -> bool:
    """Exercise 3: after Floyd-Warshall, a negative diagonal entry means a negative cycle."""
    dist, _ = floyd_warshall(n, edges)
    return any(dist[i][i] < 0 for i in range(n))


def diameter(n: int, edges: list[tuple[int, int, float]]) -> float:
    """Exercise 4: the longest of all shortest distances (finite ones)."""
    dist, _ = floyd_warshall(n, edges)
    return max(d for row in dist for d in row if d < INF)


if __name__ == "__main__":
    print(transitive_closure(3, [(0, 1), (1, 2)]))
    print(city_with_fewest_reachable(4, [(0, 1, 3), (1, 2, 1), (1, 3, 4), (2, 3, 1)], 4))
    print(has_negative_cycle(2, [(0, 1, 1), (1, 0, -2)]), diameter(3, [(0, 1, 2), (1, 2, 3)]))
