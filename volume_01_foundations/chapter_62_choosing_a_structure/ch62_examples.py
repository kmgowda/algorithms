"""Volume 1, Chapter 62 - Choosing a Data Structure.

The five questions of Figure 62.3 written as a small function.
Run:  python3 ch62_examples.py
"""

from __future__ import annotations


def recommend(*, newest_first=False, oldest_first=False, exact_keys=False, needs_order=False, extreme_only=False,
              range_totals=False, range_extremes=False, values_change=True, groups=False, on_disk=False,
              prefixes=False, tiny_memory_ok_errors=False) -> str:
    """Return the structure the five questions point to (Section 62.5)."""
    if groups:
        return "union-find"
    if range_totals:
        return "Fenwick tree" if values_change else "prefix sums"
    if range_extremes:
        return "segment tree" if values_change else "sparse table"
    if extreme_only:
        return "binary heap"
    if newest_first:
        return "stack"
    if oldest_first:
        return "queue"
    if prefixes:
        return "trie"
    if needs_order:
        return "B-tree" if on_disk else "balanced search tree"
    if exact_keys:
        return "Bloom filter" if tiny_memory_ok_errors else "hash table"
    return "array"


LIBRARY_JOBS = {
    "catalogue by call number": dict(exact_keys=True),
    "subject browsing": dict(needs_order=True, on_disk=True),
    "title autocomplete": dict(prefixes=True),
    "help-desk requests": dict(extreme_only=True),
    "returns pile / undo": dict(newest_first=True),
    "waiting list": dict(oldest_first=True),
    "visitor dashboard": dict(range_totals=True, values_change=True),
    "reading clubs": dict(groups=True),
}


if __name__ == "__main__":
    for job, needs in LIBRARY_JOBS.items():
        print(f"{job:26s} -> {recommend(**needs)}")
