"""Volume 3, Chapter 11 - The Big Comparison: Array vs. Linked List vs. Stack vs. Queue vs. Deque.

Run:  python3 ch11_examples.py
"""

from __future__ import annotations

import timeit
from collections import deque
from typing import Any, Callable


class _Node:
    __slots__ = ("value", "next")

    def __init__(self, value: Any, next_node: "_Node | None" = None) -> None:
        self.value = value
        self.next = next_node


class SinglyLinked:
    """A minimal singly linked list with a tail pointer, for fair comparisons."""

    def __init__(self) -> None:
        self.head: _Node | None = None
        self.tail: _Node | None = None
        self.size = 0

    def push_front(self, value: Any) -> None:
        self.head = _Node(value, self.head)
        if self.tail is None:
            self.tail = self.head
        self.size += 1

    def append(self, value: Any) -> None:
        node = _Node(value)
        if self.tail is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.size += 1

    def pop_front(self) -> Any:
        assert self.head is not None
        node = self.head
        self.head = node.next
        if self.head is None:
            self.tail = None
        self.size -= 1
        return node.value

    def get(self, index: int) -> Any:
        node = self.head
        for _ in range(index):
            assert node is not None
            node = node.next
        assert node is not None
        return node.value


# ------------------------------------------------------------------ the cost model (steps, same on every computer)
STEP_COSTS: dict[str, dict[str, Callable[[int], int]]] = {
    "dynamic array": {
        "get middle": lambda n: 1,
        "add front": lambda n: n,          # shift everything right
        "add back": lambda n: 1,           # amortized
        "remove front": lambda n: n,       # shift everything left
        "remove back": lambda n: 1,
        "search": lambda n: n,
    },
    "singly linked list": {
        "get middle": lambda n: n // 2,
        "add front": lambda n: 1,
        "add back": lambda n: 1,           # with a tail pointer
        "remove front": lambda n: 1,
        "remove back": lambda n: n,        # must find the node before the tail
        "search": lambda n: n,
    },
    "doubly linked list": {
        "get middle": lambda n: n // 2,
        "add front": lambda n: 1,
        "add back": lambda n: 1,
        "remove front": lambda n: 1,
        "remove back": lambda n: 1,
        "search": lambda n: n,
    },
    "deque (ring or blocks)": {
        "get middle": lambda n: n // 2,    # collections.deque: O(n) in the middle
        "add front": lambda n: 1,
        "add back": lambda n: 1,
        "remove front": lambda n: 1,
        "remove back": lambda n: 1,
        "search": lambda n: n,
    },
}


def cost_table(n: int) -> dict[str, dict[str, int]]:
    """Predicted steps for each operation at size n."""
    return {structure: {op: f(n) for op, f in ops.items()} for structure, ops in STEP_COSTS.items()}


def best_structure(needed: list[str], n: int) -> str:
    """Pick the structure with the fewest total steps for a workload of operations (cost model only)."""
    table = cost_table(n)
    return min(table, key=lambda s: sum(table[s][op] for op in needed))


# ------------------------------------------------------------------ real measurements
def time_front_operations(n: int, repeats: int = 3) -> dict[str, float]:
    """Seconds to add n items at the front and remove them all from the front."""
    def with_list() -> None:
        items: list[int] = []
        for i in range(n):
            items.insert(0, i)
        while items:
            items.pop(0)

    def with_deque() -> None:
        items: deque[int] = deque()
        for i in range(n):
            items.appendleft(i)
        while items:
            items.popleft()

    def with_linked() -> None:
        items = SinglyLinked()
        for i in range(n):
            items.push_front(i)
        while items.size:
            items.pop_front()

    return {name: min(timeit.repeat(fn, number=1, repeat=repeats))
            for name, fn in (("list", with_list), ("deque", with_deque), ("linked", with_linked))}


def time_index_middle(n: int, lookups: int = 200) -> dict[str, float]:
    """Seconds for `lookups` reads of the middle item."""
    as_list = list(range(n))
    as_deque = deque(as_list)
    as_linked = SinglyLinked()
    for i in as_list:
        as_linked.append(i)
    middle = n // 2
    return {
        "list": min(timeit.repeat(lambda: [as_list[middle] for _ in range(lookups)], number=1, repeat=3)),
        "deque": min(timeit.repeat(lambda: [as_deque[middle] for _ in range(lookups)], number=1, repeat=3)),
        "linked": min(timeit.repeat(lambda: [as_linked.get(middle) for _ in range(lookups)], number=1, repeat=3)),
    }


def choose_for(scenario: str) -> str:
    """Practical decision helper used in the chapter's decision tree."""
    rules = {
        "undo button": "stack (list end)",
        "printer jobs": "queue (deque)",
        "last 100 sensor readings": "ring buffer (deque with maxlen)",
        "seat map by number": "array (list)",
        "playlist with remove-current": "doubly linked list",
        "sliding window maximum": "monotonic deque",
        "browser back and forward": "two stacks",
    }
    return rules.get(scenario, "start with a list, measure, then decide")


if __name__ == "__main__":
    for structure, row in cost_table(1_000_000).items():
        print(f"{structure:>24}: {row}")
    print("Best for add-front + remove-back:", best_structure(["add front", "remove back"], 10_000))
    print("Best for get-middle + add-back:", best_structure(["get middle", "add back"], 10_000))
    print("Front ops, n=20,000 (seconds):", {k: round(v, 4) for k, v in time_front_operations(20_000).items()})
    print("Middle reads, n=100,000 (seconds):", {k: round(v, 5) for k, v in time_index_middle(100_000).items()})
    for scenario in ("undo button", "printer jobs", "seat map by number", "a brand-new problem"):
        print(f"{scenario!r} -> {choose_for(scenario)}")
