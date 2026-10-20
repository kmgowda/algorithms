"""Volume 1, Chapter 17 - Amortized Analysis.

Run:  python3 ch17_examples.py
"""

from __future__ import annotations


def append_costs(n: int) -> list[int]:
    """Steps for each of n appends to an array that starts with capacity 1 and doubles when full (Figure 17.1)."""
    capacity, size, costs = 1, 0, []
    for _ in range(n):
        copies = 0
        if size == capacity:
            copies = size
            capacity *= 2
        size += 1
        costs.append(1 + copies)
    return costs


def copying_with_fixed_growth(n: int, extra: int = 10, capacity: int = 10) -> int:
    """Copy steps for n appends when the array grows by `extra` spaces whenever it is full (Section 17.7)."""
    size, copies = 0, 0
    for _ in range(n):
        if size == capacity:
            copies += size
            capacity += extra
        size += 1
    return copies


if __name__ == "__main__":
    c = append_costs(33)
    print([i + 1 for i, x in enumerate(c) if x > 1], sum(c), round(sum(c) / 33, 2))
    print(sum(append_costs(10_000)) - 10_000, copying_with_fixed_growth(10_000))
