"""Volume 2, Chapter 24 - Thinking Problem solutions (Section 24.15)."""

from __future__ import annotations


def range_counter(keys: list[int], universe: int) -> list[int]:
    """Thinking Problem 24.2: P[v] = how many distinct keys are below v, for call numbers 0..universe-1.

    A presence array (direct addressing, the simplest hash) plus prefix sums: O(n + U) to build."""
    present = [0] * universe
    for k in keys:
        present[k] = 1                  # duplicates are counted once
    p = [0]
    for bit in present:
        p.append(p[-1] + bit)
    return p


def count_between(p: list[int], a: int, b: int) -> int:
    """How many keys lie in a..b inclusive, in O(1); ranges are clipped to the universe, backwards ranges give 0."""
    a, b = max(a, 0), min(b, len(p) - 2)
    return p[b + 1] - p[a] if a <= b else 0
