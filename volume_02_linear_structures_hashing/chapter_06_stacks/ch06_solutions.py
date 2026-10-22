"""Volume 2, Chapter 6 - Thinking Problems.

Problem 1: which leaving orders a pile can make (the greedy check used in the proof).
Problem 2: a stack that also reports its smallest item, every operation O(1).
Problem 3: the one-number shortcut for the smallest item, kept here so the tests can show it fails.
"""

from __future__ import annotations

from ch06_examples import Stack


def can_leave_in_order(order: list[int]) -> bool:
    """Books 1..n arrive in order and wait on one pile; can they leave in `order`? Greedy: push until wanted is on top."""
    pile, arrived = Stack(), 0
    for wanted in order:
        while arrived < wanted:
            arrived += 1
            pile.push(arrived)
        if pile.is_empty() or pile.peek() != wanted:
            return False
        pile.pop()
    return True


class MinStack:
    """A stack that also answers smallest() in O(1): a second stack holds the smallest so far at each height."""

    def __init__(self):
        self._items, self._mins = Stack(), Stack()

    def push(self, item) -> None:
        self._items.push(item)
        self._mins.push(item if self._mins.is_empty() or item < self._mins.peek() else self._mins.peek())

    def pop(self):
        self._mins.pop()
        return self._items.pop()

    def smallest(self):
        return self._mins.peek()

    def is_empty(self) -> bool:
        return self._items.is_empty()


class OneNumberMin:
    """WRONG: keeps a single `smallest`, updated on push only, so it goes stale when the smallest is popped."""

    def __init__(self):
        self._items, self._smallest = Stack(), None

    def push(self, item) -> None:
        self._items.push(item)
        if self._smallest is None or item < self._smallest:
            self._smallest = item

    def pop(self):
        return self._items.pop()

    def smallest(self):
        return self._smallest


if __name__ == "__main__":
    from itertools import permutations
    print([p for p in permutations([1, 2, 3]) if not can_leave_in_order(list(p))])
    m, w = MinStack(), OneNumberMin()
    for s in (m, w):
        for b in (47, 12, 63):
            s.push(b)
        s.pop(); s.pop()
    print(m.smallest(), w.smallest())
