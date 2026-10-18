"""Volume 3, Chapter 2 - Solutions to the exercises."""

from __future__ import annotations

from typing import Any, Iterable

from ch02_examples import DynamicArray


def extend(array: DynamicArray, values: Iterable[Any]) -> None:
    """Exercise 1: append many values."""
    for value in values:
        array.append(value)


def reverse_in_place(array: DynamicArray) -> None:
    """Exercise 2: two pointers swapping through the public interface."""
    left, right = 0, len(array) - 1
    while left < right:
        array[left], array[right] = array[right], array[left]
        left += 1
        right -= 1


def count_value(array: DynamicArray, value: Any) -> int:
    """Exercise 3."""
    return sum(1 for item in array if item == value)


def clear(array: DynamicArray) -> None:
    """Exercise 4: pop everything; watch the capacity shrink."""
    while len(array):
        array.pop()


def remove_all(array: DynamicArray, value: Any) -> int:
    """Exercise 5: remove every occurrence in ONE pass (O(n)), compacting with a write index.

    Repeated remove() would be O(n^2).
    """
    write = 0
    for read in range(len(array)):
        if array[read] != value:
            array[write] = array[read]
            write += 1
    removed = len(array) - write
    for _ in range(removed):
        array.pop()
    return removed


if __name__ == "__main__":
    a = DynamicArray()
    extend(a, [1, 2, 3, 2, 2])
    reverse_in_place(a)
    print(a, count_value(a, 2), remove_all(a, 2), a)
    clear(a)
    print(a)
