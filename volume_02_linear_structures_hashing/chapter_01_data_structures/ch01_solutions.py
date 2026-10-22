"""Volume 2, Chapter 1 - Thinking Problems.

Problem 1: shifts made by inserting into a sorted array (binary search finds the place, shifting is the cost).
Problem 2: the seat desk - occupy a chosen seat, free a seat, hand out any free seat, each in O(1).
Problem 3: shifts made by a queue kept in a list that serves from the front.
"""

from __future__ import annotations

from bisect import bisect_right


def sorted_insert_shifts(values: list[int]) -> int:
    """Total items shifted when the values are inserted one by one into a sorted array."""
    shelf: list[int] = []
    shifts = 0
    for v in values:
        place = bisect_right(shelf, v)
        shifts += len(shelf) - place
        shelf.insert(place, v)
    return shifts


class SeatDesk:
    """Seats 0 .. n-1. free[0:count] lists the free seats; where[s] is s's position there, or -1 if taken."""

    def __init__(self, n: int) -> None:
        self.free = list(range(n))
        self.where = list(range(n))
        self.count = n

    def any_free(self) -> int | None:
        return self.free[self.count - 1] if self.count else None

    def occupy(self, s: int) -> bool:
        p = self.where[s]
        if p < 0:
            return False                      # already taken
        last = self.free[self.count - 1]
        self.free[p], self.where[last] = last, p
        self.where[s] = -1
        self.count -= 1
        return True

    def leave(self, s: int) -> bool:
        if self.where[s] >= 0:
            return False                      # already free
        self.free[self.count], self.where[s] = s, self.count
        self.count += 1
        return True


def list_queue_shifts(n: int) -> int:
    """Shifts made when n people join a list-queue and then all n are served from the front."""
    line: list[int] = []
    shifts = 0
    for person in range(n):
        line.append(person)
    while line:
        shifts += len(line) - 1               # pop(0) moves everyone behind the front
        line.pop(0)
    return shifts


if __name__ == "__main__":
    print(sorted_insert_shifts([91, 84, 70, 63, 58, 47, 31, 25, 12]), list_queue_shifts(4), list_queue_shifts(1000))
    d = SeatDesk(4)
    for step in ("occupy 1", "occupy 3", "leave 1", "occupy 0"):
        op, s = step.split()
        getattr(d, op)(int(s))
        print(step, d.free[:d.count], d.where, d.any_free())
