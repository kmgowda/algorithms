"""Chapter 7 - Solutions to the exercises."""

from __future__ import annotations


def total_of(numbers: list[float]) -> float:
    """Exercise 1: add up a list without using sum()."""
    total = 0.0
    for value in numbers:
        total += value
    return total


def reverse_list(items: list[str]) -> list[str]:
    """Exercise 2: build a reversed copy with a loop (no [::-1], no reversed())."""
    result: list[str] = []
    for index in range(len(items) - 1, -1, -1):
        result.append(items[index])
    return result


def reverse_in_place(items: list[str]) -> None:
    """Exercise 3: swap from both ends towards the middle. Uses no extra list."""
    left = 0
    right = len(items) - 1
    while left < right:
        items[left], items[right] = items[right], items[left]
        left += 1
        right -= 1


def rotate_queue(people: list[str], turns: int) -> list[str]:
    """Exercise 4: the person at the front goes to the back, `turns` times."""
    if not people:
        return []
    turns %= len(people)
    return people[turns:] + people[:turns]


def column(grid: list[list[int]], index: int) -> list[int]:
    """Exercise 5: one column of a grid (e.g. one seat number across all rows)."""
    return [row[index] for row in grid]


def cart_total(prices: list[float], quantities: list[int]) -> float:
    """Exercise 6: two lists 'in step' - price i goes with quantity i."""
    if len(prices) != len(quantities):
        raise ValueError("prices and quantities must have the same length")
    total = 0.0
    for i in range(len(prices)):
        total += prices[i] * quantities[i]
    return round(total, 2)


def remove_all(items: list[str], unwanted: str) -> list[str]:
    """Exercise 7: build a new list instead of removing while looping."""
    return [item for item in items if item != unwanted]


if __name__ == "__main__":
    print(total_of([2.5, 3, 4.5]), reverse_list(["a", "b", "c"]))
    letters = ["a", "b", "c", "d"]
    reverse_in_place(letters)
    print(letters, rotate_queue(["Ana", "Ben", "Cy"], 1))
    print(column([[1, 2], [3, 4]], 1), cart_total([10.0, 2.5], [3, 4]))
    print(remove_all(["cat", "dog", "cat"], "cat"))
