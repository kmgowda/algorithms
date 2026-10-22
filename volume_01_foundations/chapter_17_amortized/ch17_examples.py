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


def copying_with_factor(n: int, factor: float, capacity: int = 1) -> tuple[int, int]:
    """(items copied, empty slots at the end) for n appends when a full array grows by `factor` (Section 17.7)."""
    size, copies = 0, 0
    for _ in range(n):
        if size == capacity:
            copies += size
            capacity = max(capacity + 1, int(capacity * factor))
        size += 1
    return copies, capacity - size


def counter_flips(n: int, bits: int = 8) -> list[int]:
    """Bits flipped by each of n increments of a binary counter that starts at 0 (Figure 17.3).

    Use enough bits (n < 2 ** bits); otherwise the counter wraps round to 0 and the count is wrong.
    """
    lamps, costs = [0] * bits, []
    for _ in range(n):
        k, flips = 0, 0
        while k < bits and lamps[k] == 1:
            lamps[k] = 0
            flips += 1
            k += 1
        if k < bits:
            lamps[k] = 1
            flips += 1
        costs.append(flips)
    return costs


def counter_amortized(n: int) -> list[int]:
    """Actual flips plus the change in potential (the number of 1 bits) for each increment (Figure 17.5)."""
    result, ones = [], 0
    for value, flips in enumerate(counter_flips(n), 1):
        new_ones = bin(value).count("1")
        result.append(flips + new_ones - ones)
        ones = new_ones
    return result


def array_amortized(n: int) -> list[int]:
    """Actual steps plus the change in potential 2 x size - capacity for each append to a doubling array."""
    def potential(size: int, capacity: int) -> int:
        return 2 * size - capacity if size else 0
    result, size, capacity = [], 0, 1
    for cost in append_costs(n):
        before = potential(size, capacity)
        if size == capacity:
            capacity *= 2
        size += 1
        result.append(cost + potential(size, capacity) - before)
    return result


if __name__ == "__main__":
    c = append_costs(33)
    print([i + 1 for i, x in enumerate(c) if x > 1], sum(c), round(sum(c) / 33, 2))
    print(sum(append_costs(10_000)) - 10_000, copying_with_fixed_growth(10_000))
    print(sum(append_costs(1000)) - 1000, sum(append_costs(1000)), sum(append_costs(32)) - 32)
    for f in (2, 1.5, 1.125):
        print(f, copying_with_factor(10_000, f))
    print(copying_with_factor(20, 1.5, 2), copying_with_factor(20, 2, 2))
    print(counter_flips(16), sum(counter_flips(8)), sum(counter_flips(16)), sum(counter_flips(1000, bits=16)))
    print(counter_amortized(16), array_amortized(17))
