"""Volume 4, Chapter 11 - The Big Comparison: Hashing vs. Sorting vs. Patterns vs. Brute Force.

Run:  python3 ch11_examples.py
"""

from __future__ import annotations

import bisect
import random
import timeit


# ------------------------------------------------------------------ one problem, three solutions
def pair_brute(values: list[int], target: int) -> bool:
    """O(n^2) time, O(1) space."""
    return any(values[i] + values[j] == target for i in range(len(values)) for j in range(i + 1, len(values)))


def pair_hash(values: list[int], target: int) -> bool:
    """O(n) average time, O(n) space."""
    seen: set[int] = set()
    for v in values:
        if target - v in seen:
            return True
        seen.add(v)
    return False


def pair_sort_two_pointers(values: list[int], target: int) -> bool:
    """O(n log n) time (sorting), O(n) space for the sorted copy (O(1) if sorting in place is allowed)."""
    s = sorted(values)
    i, j = 0, len(s) - 1
    while i < j:
        total = s[i] + s[j]
        if total == target:
            return True
        if total < target:
            i += 1
        else:
            j -= 1
    return False


# ------------------------------------------------------------------ membership: list vs set vs sorted list
def membership_times(n: int, lookups: int = 2000) -> dict[str, float]:
    """Seconds for `lookups` membership tests with three representations."""
    rng = random.Random(0)
    items = rng.sample(range(10 * n), n)
    as_list, as_set, as_sorted = items, set(items), sorted(items)
    queries = [rng.randrange(10 * n) for _ in range(lookups)]

    def in_sorted(q: int) -> bool:
        i = bisect.bisect_left(as_sorted, q)
        return i < len(as_sorted) and as_sorted[i] == q

    return {
        "list (linear scan)": min(timeit.repeat(lambda: [q in as_list for q in queries], number=1, repeat=3)),
        "sorted list (binary search)": min(timeit.repeat(lambda: [in_sorted(q) for q in queries], number=1, repeat=3)),
        "set (hashing)": min(timeit.repeat(lambda: [q in as_set for q in queries], number=1, repeat=3)),
    }


# ------------------------------------------------------------------ choosing a technique
def choose_technique(question: str, *, sorted_input: bool = False, negatives: bool = False,
                     memory_tight: bool = False) -> str:
    """A decision helper that mirrors the chapter's decision tree."""
    if question == "pair or complement":
        return "two pointers" if sorted_input or memory_tight else "hash map of seen values"
    if question == "count subarrays with exact sum":
        return "prefix sums + hash map"
    if question == "longest or shortest consecutive stretch":
        return "prefix sums + hash map" if negatives else "sliding window"
    if question == "many range totals":
        return "prefix sums"
    if question == "many range updates":
        return "difference array"
    if question == "repeat or cycle in a step sequence":
        return "fast and slow pointers"
    if question == "recently used items":
        return "LRU cache (dict + doubly linked list)"
    if question == "membership or counting":
        return "set or Counter"
    return "write the brute force first, then look for its waste"


if __name__ == "__main__":
    rng = random.Random(1)
    data = [rng.randint(0, 10**6) for _ in range(3000)]
    target = -1                                            # never found: the worst case for every method
    for fn in (pair_brute, pair_hash, pair_sort_two_pointers):
        seconds = min(timeit.repeat(lambda: fn(data, target), number=1, repeat=3))
        print(f"{fn.__name__:>24}: {seconds:.4f} s")
    print({k: round(v, 5) for k, v in membership_times(20_000).items()})
    for q in ("pair or complement", "longest or shortest consecutive stretch", "recently used items"):
        print(f"{q!r}: {choose_technique(q)}")
