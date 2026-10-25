"""Volume 4, Chapter 3 - Choosing a Data Structure.

The five questions of Figure 3.2 written as a small function.
Run:  python3 ch03_examples.py
"""

from __future__ import annotations


def recommend(*, newest_first=False, oldest_first=False, exact_keys=False, needs_order=False, extreme_only=False,
              range_totals=False, range_extremes=False, values_change=True, groups=False, on_disk=False,
              prefixes=False, tiny_memory_ok_errors=False, intervals=False, points_2d=False,
              many_decrease_keys=False, hot_keys=False, split_join=False) -> str:
    """Return the structure the five questions point to, asked in order (Section 3.5): groups and ranges
    first, then the extreme item, then which order matters (arrival, prefix, sorted, none); the
    follow-ups of question 5 (changes, disk, tiny memory, hot keys, split and join) refine the answer the
    earlier questions chose.  Volume 3, Part III adds intervals and points (question 2) and decrease-key (question 3)."""
    if groups:
        return "union-find"
    if range_totals:
        return "Fenwick tree" if values_change else "prefix sums"
    if range_extremes:
        return "segment tree" if values_change else "sparse table"
    if intervals:
        return "interval tree"
    if points_2d:
        return "k-d tree"
    if extreme_only:
        return "pairing heap" if many_decrease_keys else "binary heap"
    if newest_first:
        return "stack"
    if oldest_first:
        return "queue"
    if prefixes:
        return "trie"
    if needs_order:
        if on_disk:
            return "B-tree"
        if hot_keys:
            return "splay tree"
        return "treap" if split_join else "balanced search tree"
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


PART_III_JOBS = {
    "room bookings that overlap": dict(intervals=True),
    "nearest branch to a reader": dict(points_2d=True),
    "route planner's frontier": dict(extreme_only=True, many_decrease_keys=True),
    "popular-titles lookup": dict(needs_order=True, hot_keys=True),
    "splitting the catalogue at a call number": dict(needs_order=True, split_join=True),
}


if __name__ == "__main__":
    for job, needs in LIBRARY_JOBS.items():
        print(f"{job:26s} -> {recommend(**needs)}")
    for job, needs in PART_III_JOBS.items():
        print(f"{job:42s} -> {recommend(**needs)}")
