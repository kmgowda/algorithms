"""Volume 2, Chapter 11 - Thinking Problems.

Problem 1: a summary can live in tags exactly when it can be updated from the old summary and the new item.
Problem 2: a bag of call numbers with add, remove and pick-at-random, all O(1): an array plus a dictionary.
Problem 3: the space-saving min-stack that pushes a new minimum only when it is strictly smaller, kept here
so the tests can show it.
"""

from __future__ import annotations

import random


def distinct_count_is_not_a_tag() -> tuple[int, int, int, int]:
    """Two piles with the same distinct count (1) that differ after the same push: no tag rule can exist."""
    a, b = [1], [2]
    return len(set(a)), len(set(b)), len(set(a + [1])), len(set(b + [1]))


class RandomBag:
    """Invariant: items[pos[x]] == x for every x in the bag, and items holds each x exactly once."""

    def __init__(self, rng: random.Random | None = None):
        self.items: list = []
        self.pos: dict = {}
        self.rng = rng or random.Random()

    def add(self, x) -> bool:
        if x in self.pos:
            return False
        self.pos[x] = len(self.items)
        self.items.append(x)
        return True

    def remove(self, x) -> bool:
        if x not in self.pos:
            return False
        i, last = self.pos.pop(x), self.items.pop()
        if last != x:                       # move the last item into the hole left by x
            self.items[i] = last
            self.pos[last] = i
        return True

    def pick(self):
        if not self.items:
            raise IndexError("pick from an empty bag")
        return self.items[self.rng.randrange(len(self.items))]

    def __len__(self) -> int:
        return len(self.items)


class SparseMinStackBuggy:
    """WRONG: records a new minimum only when it is strictly smaller, so a repeated minimum is lost."""

    def __init__(self):
        self.items: list[int] = []
        self.mins: list[int] = []

    def push(self, v: int) -> None:
        self.items.append(v)
        if not self.mins or v < self.mins[-1]:     # the fix: v <= self.mins[-1]
            self.mins.append(v)

    def pop(self) -> int:
        v = self.items.pop()
        if v == self.mins[-1]:
            self.mins.pop()
        return v

    def min(self) -> int:
        return self.mins[-1]


if __name__ == "__main__":
    print(distinct_count_is_not_a_tag())
    bag = RandomBag(random.Random(11))
    for c in (47, 63, 12, 25):
        bag.add(c)
    bag.remove(63)
    print(bag.items, bag.pos, bag.pick())
    s = SparseMinStackBuggy()
    for v in (30, 20, 20, 40):
        s.push(v)
    s.pop(); s.pop()
    print(s.items, s.min())
