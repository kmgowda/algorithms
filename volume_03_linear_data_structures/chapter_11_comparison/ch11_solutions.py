"""Volume 3, Chapter 11 - Solutions to the exercises."""

from __future__ import annotations

from ch11_examples import cost_table


def total_steps(structure: str, workload: dict[str, int], n: int) -> int:
    """Exercise 1: weighted cost of a workload {operation: how many times}."""
    table = cost_table(n)[structure]
    return sum(table[op] * times for op, times in workload.items())


def ranking(workload: dict[str, int], n: int) -> list[str]:
    """Exercise 2: structures from cheapest to most expensive for a workload."""
    return sorted(cost_table(n), key=lambda s: total_steps(s, workload, n))


def crossover_size(workload_a: dict[str, int], structure_a: str, structure_b: str, limit: int = 100_000) -> int | None:
    """Exercise 3: the smallest n at which structure_b becomes cheaper than structure_a for a workload."""
    for n in range(1, limit):
        if total_steps(structure_b, workload_a, n) < total_steps(structure_a, workload_a, n):
            return n
    return None


if __name__ == "__main__":
    taxi = {"add back": 1000, "remove front": 1000}
    print(total_steps("dynamic array", taxi, 500), ranking(taxi, 500))
    print(crossover_size({"get middle": 10, "add front": 1}, "singly linked list", "dynamic array"))
