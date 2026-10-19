"""Volume 15, Chapter 8 - Solutions to the exercises."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor


def parallel_max(values: list[int], chunks: int) -> int:
    """Exercise 1: fork-join maximum - each task finds a chunk's max, the join takes the max of maxima.
    (Threads are fine for demonstrating structure; use processes for real CPU-bound speed-ups in Python.)"""
    size = max(1, -(-len(values) // chunks))
    parts = [values[i:i + size] for i in range(0, len(values), size)]
    with ThreadPoolExecutor(chunks) as pool:
        return max(pool.map(max, parts))


def work_and_span_sum(n: int) -> tuple[int, int]:
    """Exercise 2: summing n numbers as a balanced tree of additions - work n - 1, span ceil(log2 n)."""
    work, span, level = 0, 0, n
    while level > 1:
        work += level // 2
        level = -(-level // 2)
        span += 1
    return work, span


def max_useful_processors(parallel_fraction: float, target: float) -> int | None:
    """Exercise 3: fewest processors reaching a target speed-up under Amdahl's law, or None if impossible."""
    limit = 1 / (1 - parallel_fraction) if parallel_fraction < 1 else float("inf")
    if target >= limit - 1e-9:                         # tolerance: 1 / (1 - 0.9) is 10.000000000000002 in floats
        return None
    p = 1
    while 1 / ((1 - parallel_fraction) + parallel_fraction / p) < target:
        p += 1
    return p


if __name__ == "__main__":
    print(parallel_max([3, 9, 2, 7, 11, 4], 3), work_and_span_sum(8), max_useful_processors(0.9, 5), max_useful_processors(0.9, 10))
