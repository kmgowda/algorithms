"""Volume 8, Chapter 7 - Solutions to the exercises."""

from __future__ import annotations

from collections import deque

from ch07_examples import Graph, topological_sort_kahn


def can_finish(n: int, prerequisites: list[tuple[int, int]]) -> bool:
    """Exercise 1 (LeetCode 207): possible exactly when the prerequisite graph has no cycle."""
    graph: Graph = {c: [] for c in range(n)}
    for course, pre in prerequisites:
        graph[pre].append(course)
    return topological_sort_kahn(graph) is not None


def semesters_needed(n: int, prerequisites: list[tuple[int, int]]) -> int:
    """Exercise 2 (LeetCode 1136): take any number of ready courses per semester. Kahn's algorithm in levels."""
    graph: Graph = {c: [] for c in range(n)}
    indegree = {c: 0 for c in range(n)}
    for course, pre in prerequisites:
        graph[pre].append(course)
        indegree[course] += 1
    ready = deque(c for c in range(n) if indegree[c] == 0)
    semesters, taken = 0, 0
    while ready:
        semesters += 1
        for _ in range(len(ready)):
            c = ready.popleft()
            taken += 1
            for nxt in graph[c]:
                indegree[nxt] -= 1
                if indegree[nxt] == 0:
                    ready.append(nxt)
    return semesters if taken == n else -1


def alien_alphabet(words: list[str]) -> str:
    """Exercise 3 (LeetCode 269): words are sorted in an unknown alphabet; recover a letter order."""
    graph: Graph = {ch: [] for w in words for ch in w}
    for a, b in zip(words, words[1:]):
        for x, y in zip(a, b):
            if x != y:
                if y not in graph[x]:
                    graph[x].append(y)
                break
        else:
            if len(a) > len(b):
                return ""                               # 'abc' before 'ab' is impossible
    order = topological_sort_kahn(graph)
    return "".join(order) if order is not None else ""  # type: ignore[arg-type]


def is_valid_order(graph: Graph, order: list) -> bool:
    """Exercise 4: check an order: every edge u -> v must have u before v."""
    pos = {v: i for i, v in enumerate(order)}
    return len(pos) == len(graph) and all(pos[u] < pos[v] for u in graph for v in graph[u])


if __name__ == "__main__":
    print(can_finish(2, [(1, 0)]), can_finish(2, [(1, 0), (0, 1)]), semesters_needed(3, [(2, 0), (2, 1)]))
    print(alien_alphabet(["wrt", "wrf", "er", "ett", "rftt"]))
