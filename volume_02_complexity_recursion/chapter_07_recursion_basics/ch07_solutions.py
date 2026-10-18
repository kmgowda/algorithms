"""Volume 2, Chapter 7 - Solutions to the exercises."""

from __future__ import annotations

from typing import Any


def count_up(n: int) -> list[int]:
    """Exercise 1: 1, 2, ..., n - the recursive call comes BEFORE adding n."""
    if n == 0:
        return []
    return count_up(n - 1) + [n]


def digit_sum(n: int) -> int:
    """Exercise 2: digit_sum(4096) = 6 + digit_sum(409)."""
    if n < 10:
        return n
    return n % 10 + digit_sum(n // 10)


def count_occurrences(items: list[str], target: str) -> int:
    """Exercise 3: occurrences = (1 if the first matches) + occurrences in the rest."""
    if not items:
        return 0
    return (1 if items[0] == target else 0) + count_occurrences(items[1:], target)


def power(base: float, exponent: int) -> float:
    """Exercise 4: base^exponent = base x base^(exponent - 1). (Chapter 9 makes this much faster.)"""
    if exponent < 0:
        raise ValueError("non-negative exponents only")
    if exponent == 0:
        return 1
    return base * power(base, exponent - 1)


def deepest_level(folder: dict[str, Any]) -> int:
    """Exercise 5: how many folders deep does this folder go? A folder with no sub-folders is depth 1."""
    sub_folders = folder.get("folders", {}).values()
    return 1 + max((deepest_level(sub) for sub in sub_folders), default=0)


def find_person(person: dict[str, Any], name: str) -> list[str] | None:
    """Exercise 6: the chain of managers from the top down to `name`, or None if not found."""
    if person["name"] == name:
        return [name]
    for report in person.get("reports", []):
        chain = find_person(report, name)
        if chain is not None:
            return [person["name"]] + chain
    return None


if __name__ == "__main__":
    print(count_up(5), digit_sum(4096), count_occurrences(["cat", "dog", "cat"], "cat"), power(2, 10))
    from ch07_examples import SAMPLE_DISK, SAMPLE_ORG
    print(deepest_level(SAMPLE_DISK), find_person(SAMPLE_ORG, "Nurse B"))
