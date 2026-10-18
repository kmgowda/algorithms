"""Volume 2, Chapter 11 - Solutions to the exercises."""

from __future__ import annotations

from ch11_examples import simulate_appends


def copies_with_factor(n: int, factor: float) -> int:
    """Exercise 2: total copies when capacity grows by `factor` (e.g. 1.5) each time it fills."""
    capacity, size, copies = 1, 0, 0
    for _ in range(n):
        if size == capacity:
            copies += size
            capacity = max(capacity + 1, int(capacity * factor))
        size += 1
    return copies


def thrashing_cost(operations: int, shrink_when: float) -> int:
    """Exercise 4: alternate append/pop at a capacity boundary.

    The array doubles when full and halves when its fill drops to `shrink_when` of capacity or less.
    Returns total copies. shrink_when = 0.5 thrashes; 0.25 does not.
    """
    capacity, size, copies = 4, 4, 0              # start exactly full
    for step in range(operations):
        if step % 2 == 0:                          # append
            if size == capacity:
                copies += size
                capacity *= 2
            size += 1
        else:                                      # pop
            size -= 1
            if capacity > 4 and size <= capacity * shrink_when:
                copies += size
                capacity //= 2
    return copies


def restock_amortized(days: int, daily_sales: int, truck_capacity: int, truck_cost: int) -> float:
    """Exercise 5: a shop pays `truck_cost` whenever stock runs out and a truck refills it."""
    stock, total = truck_capacity, 0
    for _ in range(days):
        stock -= daily_sales
        if stock < daily_sales:
            total += truck_cost
            stock = truck_capacity
    return total / days


def worst_vs_amortized(n: int) -> tuple[int, float]:
    """Exercise 1: worst single append vs. amortized cost, with doubling."""
    stats = simulate_appends(n)
    return stats["worst_single_append"], (n + stats["copies"]) / n


if __name__ == "__main__":
    print(copies_with_factor(100_000, 1.5), copies_with_factor(100_000, 2))
    print(thrashing_cost(1000, 0.5), thrashing_cost(1000, 0.25))
    print(restock_amortized(365, 40, 1000, 500), worst_vs_amortized(1_000_000))
