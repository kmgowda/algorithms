"""Volume 5, Chapter 12 - Every Sort Side by Side: Measurements and a Decision Tree.

Compact copies of the volume's sorts live here so this chapter can race them in one file.

Run:  python3 ch12_examples.py
"""

from __future__ import annotations

import heapq
import random
import timeit
from typing import Callable


def insertion_sort(a: list) -> list:
    a = list(a)
    for i in range(1, len(a)):
        card, j = a[i], i - 1
        while j >= 0 and a[j] > card:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = card
    return a


def merge_sort(a: list) -> list:
    if len(a) <= 1:
        return list(a)
    mid = len(a) // 2
    left, right = merge_sort(a[:mid]), merge_sort(a[mid:])
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    return out + left[i:] + right[j:]


def quick_sort(a: list, rng: random.Random = random.Random(0)) -> list:
    if len(a) <= 1:
        return list(a)
    pivot = rng.choice(a)
    return (quick_sort([x for x in a if x < pivot], rng) + [x for x in a if x == pivot]
            + quick_sort([x for x in a if x > pivot], rng))


def heap_sort(a: list) -> list:
    h = list(a)
    heapq.heapify(h)
    return [heapq.heappop(h) for _ in range(len(h))]


def radix_sort(a: list) -> list:
    """Non-negative integers only."""
    out, place = list(a), 1
    while out and max(out) // place:
        buckets: list[list[int]] = [[] for _ in range(10)]
        for v in out:
            buckets[(v // place) % 10].append(v)
        out = [v for b in buckets for v in b]
        place *= 10
    return out


SORTS: dict[str, Callable[[list], list]] = {
    "insertion": insertion_sort, "merge": merge_sort, "quick": quick_sort,
    "heap": heap_sort, "radix": radix_sort, "built-in sorted (Timsort)": sorted,
}


def make_input(kind: str, n: int, seed: int = 1) -> list[int]:
    rng = random.Random(seed)
    if kind == "random":
        return [rng.randrange(10 * n) for _ in range(n)]
    if kind == "sorted":
        return list(range(n))
    if kind == "reversed":
        return list(range(n, 0, -1))
    if kind == "nearly sorted":
        a = list(range(n))
        for _ in range(max(1, n // 100)):
            i, j = rng.randrange(n), rng.randrange(n)
            a[i], a[j] = a[j], a[i]
        return a
    if kind == "few distinct":
        return [rng.randrange(5) for _ in range(n)]
    raise ValueError(kind)


def race(n: int, kinds: list[str], sorts: list[str] | None = None) -> dict[str, dict[str, float]]:
    """Seconds for each sort on each input kind (best of 3)."""
    sorts = sorts or list(SORTS)
    results: dict[str, dict[str, float]] = {}
    for name in sorts:
        results[name] = {}
        for kind in kinds:
            data = make_input(kind, n)
            results[name][kind] = min(timeit.repeat(lambda: SORTS[name](data), number=1, repeat=3))
    return results


def recommend(*, n: int, need_stable: bool = False, memory_tight: bool = False, small_int_keys: bool = False,
              nearly_sorted: bool = False, worst_case_guarantee: bool = False) -> str:
    """The chapter's decision tree as code."""
    if n <= 32:
        return "insertion sort"
    if small_int_keys:
        return "counting or radix sort"
    if nearly_sorted or need_stable:
        return "Timsort (Python's sorted)"
    if memory_tight and worst_case_guarantee:
        return "heapsort"
    if memory_tight:
        return "quicksort (random pivot or introsort)"
    return "Timsort (Python's sorted) - the default"


if __name__ == "__main__":
    kinds = ["random", "sorted", "nearly sorted", "few distinct"]
    for name, row in race(3000, kinds).items():
        print(f"{name:>26}: " + "  ".join(f"{k}={v * 1000:7.1f}ms" for k, v in row.items()))
    print(recommend(n=10), "|", recommend(n=10**6, small_int_keys=True), "|", recommend(n=10**6, memory_tight=True, worst_case_guarantee=True))
