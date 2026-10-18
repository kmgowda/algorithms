"""Chapter 9 - Solutions to the exercises."""

from __future__ import annotations



def smallest(values: list[float]) -> float:
    """Exercise 1: the minimum, without min()."""
    if not values:
        raise ValueError("empty list")
    best = values[0]
    for value in values[1:]:
        if value < best:
            best = value
    return best


def count_above(values: list[float], threshold: float) -> int:
    """Exercise 2: how many days were hotter than the threshold?"""
    count = 0
    for value in values:
        if value > threshold:
            count += 1
    return count


def last_index_of(items: list[str], target: str) -> int:
    """Exercise 3: search from the back so we can stop at the first match we meet."""
    for index in range(len(items) - 1, -1, -1):
        if items[index] == target:
            return index
    return -1


def longest_word(sentence: str) -> str:
    """Exercise 4: the longest word (first one wins ties)."""
    best = ""
    for word in sentence.split():
        if len(word) > len(best):
            best = word
    return best


def is_sorted(values: list[int]) -> bool:
    """Exercise 5: each neighbor pair must be in order; stop at the first pair that is not."""
    for i in range(len(values) - 1):
        if values[i] > values[i + 1]:
            return False
    return True


def min_and_max(values: list[int]) -> tuple[int, int]:
    """Exercise 6: both in one pass."""
    if not values:
        raise ValueError("empty list")
    low = high = values[0]
    for value in values[1:]:
        if value < low:
            low = value
        elif value > high:
            high = value
    return low, high


def best_profit(prices: list[int]) -> int:
    """Exercise 7 (challenge): buy one day, sell a later day. Track the cheapest price so far."""
    cheapest_so_far: int | None = None
    best = 0
    for price in prices:
        if cheapest_so_far is None or price < cheapest_so_far:
            cheapest_so_far = price
        elif price - cheapest_so_far > best:
            best = price - cheapest_so_far
    return best


if __name__ == "__main__":
    print(smallest([4, -2, 7]), count_above([31, 28, 35, 30], 30), last_index_of(["a", "b", "a"], "a"))
    print(longest_word("the hippopotamus ate grass"), is_sorted([1, 2, 2, 5]), min_and_max([3, 9, 1]))
    print(best_profit([7, 1, 5, 3, 6, 4]))
