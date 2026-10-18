"""Volume 10, Chapter 3 - Solutions to the exercises."""

from __future__ import annotations

import itertools

from ch03_examples import total_waiting


def weighted_waiting_order(durations: list[int], weights: list[int]) -> list[int]:
    """Exercise 1 (Smith's rule): minimise sum of weight x finish time - order by duration / weight.
    Exchange argument: neighbours i, j should swap if d_i * w_j > d_j * w_i."""
    return sorted(range(len(durations)), key=lambda i: durations[i] / weights[i])


def weighted_cost(durations: list[int], weights: list[int], order: list[int]) -> int:
    clock = total = 0
    for i in order:
        clock += durations[i]
        total += weights[i] * clock
    return total


def counterexample_longest_first(durations: list[int]) -> tuple[int, int]:
    """Exercise 2: 'longest job first' is worse - (its waiting, the optimum)."""
    longest = sorted(range(len(durations)), key=lambda i: -durations[i])
    best = min(total_waiting(durations, list(p)) for p in itertools.permutations(range(len(durations))))
    return total_waiting(durations, longest), best


def find_inversion(order: list[int], deadlines: list[int]) -> tuple[int, int] | None:
    """Exercise 3: the first adjacent pair where a later deadline comes before an earlier one."""
    for a, b in zip(order, order[1:]):
        if deadlines[a] > deadlines[b]:
            return a, b
    return None


if __name__ == "__main__":
    print(weighted_waiting_order([3, 1, 2], [1, 3, 1]), counterexample_longest_first([5, 1, 3]),
          find_inversion([2, 0, 1], [6, 8, 9]))
