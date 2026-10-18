"""Volume 10, Chapter 1 - Solutions to the exercises."""

from __future__ import annotations


def find_max_divide(values: list[int]) -> int:
    """Exercise 1: largest value by divide and conquer - the max of the two halves' maxima."""
    if len(values) == 1:
        return values[0]
    mid = len(values) // 2
    return max(find_max_divide(values[:mid]), find_max_divide(values[mid:]))


def power_decrease(base: int, exp: int) -> int:
    """Exercise 2: decrease-and-conquer by a factor - halve the exponent (V2-C9)."""
    if exp == 0:
        return 1
    half = power_decrease(base, exp // 2)
    return half * half * (base if exp % 2 else 1)


def has_duplicates_transform(values: list[int]) -> bool:
    """Exercise 3: transform-and-conquer - sort first, then duplicates are neighbours."""
    s = sorted(values)
    return any(a == b for a, b in zip(s, s[1:]))


def classify(description: str) -> str:
    """Exercise 4: name the paradigm from a one-line description."""
    rules = [("half", "divide and conquer"), ("best-looking", "greedy"), ("undo", "backtracking"),
             ("remember", "dynamic programming"), ("sort first", "transform and conquer"),
             ("every", "brute force")]
    for key, paradigm in rules:
        if key in description:
            return paradigm
    return "unknown"


if __name__ == "__main__":
    print(find_max_divide([4, 9, 2, 7]), power_decrease(3, 13), has_duplicates_transform([3, 1, 3]),
          classify("split the list in half and merge"))
