"""Volume 8, Chapter 4 - Solutions to the exercises."""

from __future__ import annotations

from typing import Hashable

from ch04_examples import Graph, dfs_iterative


def all_paths(graph: Graph, start: Hashable, goal: Hashable) -> list[list[Hashable]]:
    """Exercise 1 (LeetCode 797): every path from start to goal in a DAG - DFS that builds the path as it goes."""
    out: list[list[Hashable]] = []
    path = [start]

    def visit(v: Hashable) -> None:
        if v == goal:
            out.append(list(path))
            return
        for w in graph.get(v, []):
            path.append(w)
            visit(w)
            path.pop()                                  # undo the step (backtracking, Volume 11)

    visit(start)
    return out


def count_components(graph: Graph) -> int:
    """Exercise 2: start a DFS from every vertex not yet seen; each start is a new component."""
    seen: set[Hashable] = set()
    count = 0
    for v in graph:
        if v not in seen:
            seen.update(dfs_iterative(graph, v))
            count += 1
    return count


def clone_graph(graph: Graph) -> Graph:
    """Exercise 3 (LeetCode 133 idea): copy every vertex and edge, visiting each vertex once."""
    copy: Graph = {}
    for v in graph:
        if v not in copy:
            for u in dfs_iterative(graph, v):
                copy[u] = list(graph.get(u, []))
    return copy


def depth_of_dfs_tree(graph: Graph, start: Hashable) -> int:
    """Exercise 4: how deep does recursive DFS go? (Why recursion can overflow on long chains.)
    A stack of neighbour iterators mimics the call stack exactly; its length is the recursion depth."""
    visited, stack, deepest = {start}, [iter(graph.get(start, []))], 0
    while stack:
        deepest = max(deepest, len(stack) - 1)
        w = next(stack[-1], None)
        if w is None:
            stack.pop()
        elif w not in visited:
            visited.add(w)
            stack.append(iter(graph.get(w, [])))
    return deepest


if __name__ == "__main__":
    print(all_paths({0: [1, 2], 1: [3], 2: [3], 3: []}, 0, 3))
    print(count_components({1: [2], 2: [1], 3: [], 4: [5], 5: [4]}), clone_graph({"a": ["b"], "b": ["a"]}),
          depth_of_dfs_tree({i: [i + 1] for i in range(10)} | {10: []}, 0))
