"""Volume 15, Chapter 4 - Solutions to the exercises."""

from __future__ import annotations


def greedy_bin_packing(items: list[float], capacity: float) -> list[list[float]]:
    """Exercise 1: first-fit decreasing - largest items first, each into the first bin with room.
    Uses at most 11/9 OPT + 1 bins (a classic result)."""
    bins: list[list[float]] = []
    space: list[float] = []
    for x in sorted(items, reverse=True):
        for i, free in enumerate(space):
            if x <= free:
                bins[i].append(x)
                space[i] -= x
                break
        else:
            bins.append([x])
            space.append(capacity - x)
    return bins


def greedy_vertex_cover_bad(edges: list[tuple[int, int]]) -> set[int]:
    """Exercise 2: 'take the vertex with most uncovered edges' sounds smarter but has NO constant-factor
    guarantee (it can be about log n times worse); this is set cover's greedy in disguise."""
    remaining, cover = list(edges), set()
    while remaining:
        degree: dict[int, int] = {}
        for u, v in remaining:
            degree[u] = degree.get(u, 0) + 1
            degree[v] = degree.get(v, 0) + 1
        best = max(degree, key=lambda x: (degree[x], -x))
        cover.add(best)
        remaining = [(u, v) for u, v in remaining if best not in (u, v)]
    return cover


def load_balancing_lpt(jobs: list[int], machines: int) -> int:
    """Exercise 3: longest processing time first onto the least loaded machine - makespan <= 4/3 OPT."""
    loads = [0] * machines
    for j in sorted(jobs, reverse=True):
        loads[loads.index(min(loads))] += j
    return max(loads)


if __name__ == "__main__":
    print(greedy_bin_packing([0.5, 0.7, 0.5, 0.2, 0.4, 0.2, 0.5, 0.1], 1.0), load_balancing_lpt([7, 5, 4, 4, 3, 3], 3),
          greedy_vertex_cover_bad([(0, 1), (0, 2), (1, 2)]))
