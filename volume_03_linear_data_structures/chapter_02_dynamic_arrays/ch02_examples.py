"""Volume 3, Chapter 2 - Arrays and Dynamic Arrays: building our own Python list.

The fixed-size block of slots is simulated with a Python list of a set length (`[None] * capacity`)
that we never resize directly - every growth is an explicit copy, exactly as in a real array.

Run:  python3 ch02_examples.py
"""

from __future__ import annotations

from typing import Any, Iterator


class DynamicArray:
    """A growable array. Invariants: 0 <= size <= capacity, and slots[0:size] hold the items."""

    def __init__(self, capacity: int = 4) -> None:
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        self._slots: list[Any] = [None] * capacity
        self._size = 0
        self.copies = 0                     # how many items have been copied by resizes (for teaching)

    # -------------------------------------------------- size and capacity
    def __len__(self) -> int:
        return self._size

    @property
    def capacity(self) -> int:
        return len(self._slots)

    def _resize(self, new_capacity: int) -> None:
        new_slots: list[Any] = [None] * new_capacity
        for i in range(self._size):          # copy every item: O(n)
            new_slots[i] = self._slots[i]
        self.copies += self._size
        self._slots = new_slots

    def _check_index(self, index: int) -> int:
        if index < 0:
            index += self._size              # support negative indexes like Python lists
        if not 0 <= index < self._size:
            raise IndexError("index out of range")
        return index

    # -------------------------------------------------- reading and writing by index: O(1)
    def __getitem__(self, index: int) -> Any:
        return self._slots[self._check_index(index)]

    def __setitem__(self, index: int, value: Any) -> None:
        self._slots[self._check_index(index)] = value

    # -------------------------------------------------- adding
    def append(self, value: Any) -> None:
        """Amortized O(1): double the capacity when full (V2-C11)."""
        if self._size == self.capacity:
            self._resize(2 * self.capacity)
        self._slots[self._size] = value
        self._size += 1

    def insert(self, index: int, value: Any) -> None:
        """O(n - index): shift everything after `index` one slot to the right."""
        if not 0 <= index <= self._size:
            raise IndexError("index out of range")
        if self._size == self.capacity:
            self._resize(2 * self.capacity)
        for i in range(self._size, index, -1):
            self._slots[i] = self._slots[i - 1]
        self._slots[index] = value
        self._size += 1

    # -------------------------------------------------- removing
    def pop(self, index: int = -1) -> Any:
        """Remove and return an item. O(1) at the end, O(n - index) elsewhere. Shrinks at 1/4 full."""
        index = self._check_index(index)
        value = self._slots[index]
        for i in range(index, self._size - 1):
            self._slots[i] = self._slots[i + 1]
        self._slots[self._size - 1] = None   # don't keep a reference to removed items
        self._size -= 1
        if self.capacity > 4 and self._size <= self.capacity // 4:
            self._resize(self.capacity // 2)
        return value

    def remove(self, value: Any) -> None:
        """Remove the first occurrence of value. O(n)."""
        for i in range(self._size):
            if self._slots[i] == value:
                self.pop(i)
                return
        raise ValueError(f"{value!r} not found")

    # -------------------------------------------------- searching and iterating
    def index(self, value: Any) -> int:
        for i in range(self._size):
            if self._slots[i] == value:
                return i
        raise ValueError(f"{value!r} not found")

    def __contains__(self, value: Any) -> bool:
        return any(self._slots[i] == value for i in range(self._size))

    def __iter__(self) -> Iterator[Any]:
        for i in range(self._size):
            yield self._slots[i]

    def __repr__(self) -> str:
        return f"DynamicArray({list(self)}, capacity={self.capacity})"


# ------------------------------------------------------------------ examples using the class
def sensor_log(readings: list[float]) -> DynamicArray:
    """Industry example: a device logs temperature readings as they arrive."""
    log = DynamicArray(capacity=2)
    for reading in readings:
        log.append(reading)
    return log


def boarding_order(passengers: list[str], priority: list[str]) -> list[str]:
    """Practical example: priority passengers are inserted at the front of the boarding list."""
    queue = DynamicArray()
    for name in passengers:
        queue.append(name)
    for position, name in enumerate(priority):
        queue.insert(position, name)
    return list(queue)


if __name__ == "__main__":
    shelf = DynamicArray(capacity=2)
    for book in ["Atlas", "Birds", "Cats", "Dune", "Emma"]:
        shelf.append(book)
        print(f"after appending {book!r}: size={len(shelf)}, capacity={shelf.capacity}, copies={shelf.copies}")
    shelf.insert(1, "Aesop")
    print(shelf, "| shelf[-1] =", shelf[-1], "| 'Dune' in shelf:", "Dune" in shelf)
    print("popped:", shelf.pop(0), "->", shelf)
    log = sensor_log([20.5 + i / 10 for i in range(1000)])
    print(f"1000 readings: capacity={log.capacity}, copies={log.copies} (under 2 per append)")
    print(boarding_order(["Ana", "Ben", "Cy"], ["Wheelchair user", "Family with baby"]))
