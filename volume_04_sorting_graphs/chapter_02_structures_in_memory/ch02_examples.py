"""Volume 4, Chapter 2 - Structures in Memory: locality and caches.

Run:  python3 ch02_examples.py
"""

from __future__ import annotations

import array
import random
import sys
import time


class Node:
    __slots__ = ("value", "next")

    def __init__(self, value, nxt=None):
        self.value, self.next = value, nxt


def build_chain(values, shuffle_memory: bool = False, seed: int = 1):
    """A linked list of the values. With shuffle_memory, nodes are created in random order, so neighbours in the
    list are scattered in memory (Figure 2.2)."""
    nodes = [None] * len(values)
    order = list(range(len(values)))
    if shuffle_memory:
        random.Random(seed).shuffle(order)
    for i in order:
        nodes[i] = Node(values[i])
    for i in range(len(values) - 1):
        nodes[i].next = nodes[i + 1]
    return nodes[0] if nodes else None


def sum_chain(head) -> int:
    total = 0
    while head is not None:
        total += head.value
        head = head.next
    return total


def grid_sums(grid) -> tuple[int, int]:
    """Row by row (along memory) and column by column (jumping between rows)."""
    if not grid:                                      # no rows: nothing to add, and no grid[0] to measure
        return 0, 0
    rows, cols = len(grid), len(grid[0])
    by_rows = sum(grid[r][c] for r in range(rows) for c in range(cols))
    by_cols = sum(grid[r][c] for c in range(cols) for r in range(rows))
    return by_rows, by_cols


def bytes_per_item(n: int = 100_000) -> dict:
    """Approximate memory per stored number for three containers."""
    values = list(range(1000, 1000 + n))
    lst = sys.getsizeof(values) + sum(sys.getsizeof(v) for v in values)
    arr = sys.getsizeof(array.array("q", values))
    head = build_chain(values)
    chain = n * (sys.getsizeof(head) + sys.getsizeof(1000))
    return {"array.array": arr / n, "list": lst / n, "linked list": chain / n}


def timed(fn, *args, repeat: int = 3) -> float:
    best = float("inf")
    for _ in range(repeat):
        t = time.perf_counter()
        fn(*args)
        best = min(best, time.perf_counter() - t)
    return best * 1e3


def experiment(n: int = 1_000_000, side: int = 1000) -> dict:
    values = list(range(n))
    arr = array.array("q", values)
    near = build_chain(values)
    far = build_chain(values, shuffle_memory=True)
    grid = [[1] * side for _ in range(side)]
    rows, cols = side, side
    return {
        "sum array.array": timed(sum, arr),
        "sum list": timed(sum, values),
        "walk chain, nodes in order": timed(sum_chain, near),
        "walk chain, nodes scattered": timed(sum_chain, far),
        "grid row by row": timed(lambda: sum(grid[r][c] for r in range(rows) for c in range(cols))),
        "grid column by column": timed(lambda: sum(grid[r][c] for c in range(cols) for r in range(rows))),
    }


class Loan:
    __slots__ = ("day", "call_number", "reader", "next")

    def __init__(self, day, call_number, reader):
        self.day, self.call_number, self.reader, self.next = day, call_number, reader, None


def loan_report(n: int = 200_000, days: int = 365, seed: int = 1) -> dict:
    """Section 2.9: loans per day from a linked list of scattered records versus parallel arrays."""
    rng = random.Random(seed)
    day_of = sorted(rng.randrange(days) for _ in range(n))
    calls = [rng.randrange(1000) for _ in range(n)]
    readers = [rng.randrange(50_000) for _ in range(n)]
    records = [Loan(d, c, r) for d, c, r in zip(day_of, calls, readers)]
    order = list(range(n))
    rng.shuffle(order)
    scattered = [None] * n
    for i in order:                                   # allocate in shuffled order, then link in date order
        scattered[i] = Loan(records[i].day, records[i].call_number, records[i].reader)
    for i in range(n - 1):
        scattered[i].next = scattered[i + 1]
    head = scattered[0]
    day_arr = array.array("l", day_of)

    def from_list():
        counts = [0] * days
        node = head
        while node is not None:
            counts[node.day] += 1
            node = node.next
        return counts

    def from_arrays():
        counts = [0] * days
        for d in day_arr:
            counts[d] += 1
        return counts

    assert from_list() == from_arrays()
    return {"linked records ms": timed(from_list), "parallel arrays ms": timed(from_arrays)}


if __name__ == "__main__":
    print(loan_report())
    print({k: round(v, 1) for k, v in bytes_per_item().items()})
    for k, v in experiment().items():
        print(f"{k:30s} {v:8.1f} ms")
