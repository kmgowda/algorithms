"""Volume 5, Chapter 12 - Solutions to the exercises."""

from __future__ import annotations

import timeit

from ch12_examples import SORTS, make_input


def doubling_ratio(sort_name: str, n: int) -> float:
    """Exercise 1 (V2-C1's doubling experiment): time(2n) / time(n). About 2 for n log n sorts, about 4 for n^2."""
    small, big = make_input("random", n), make_input("random", 2 * n)
    t1 = min(timeit.repeat(lambda: SORTS[sort_name](small), number=1, repeat=3))
    t2 = min(timeit.repeat(lambda: SORTS[sort_name](big), number=1, repeat=3))
    return t2 / t1


def crossover(slow: str, fast: str, sizes: list[int]) -> int | None:
    """Exercise 2: the first size at which `fast` actually beats `slow` on random data."""
    for n in sizes:
        data = make_input("random", n)
        t_slow = min(timeit.repeat(lambda: SORTS[slow](data), number=3, repeat=3))
        t_fast = min(timeit.repeat(lambda: SORTS[fast](data), number=3, repeat=3))
        if t_fast < t_slow:
            return n
    return None


if __name__ == "__main__":
    print(round(doubling_ratio("insertion", 1000), 1), round(doubling_ratio("merge", 4000), 1))
    print(crossover("insertion", "merge", [4, 8, 16, 32, 64, 128, 256]))
