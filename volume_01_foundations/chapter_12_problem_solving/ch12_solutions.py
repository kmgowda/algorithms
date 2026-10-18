"""Chapter 12 - Solutions to the exercises (each solved with the SPIRAL method)."""

from __future__ import annotations


def contains_duplicate(ids: list[int]) -> bool:
    """Exercise 1 (LeetCode 217). Refined: O(n) with a set (brute force compares all pairs)."""
    seen: set[int] = set()
    for item in ids:
        if item in seen:
            return True
        seen.add(item)
    return False


def is_clean_palindrome(text: str) -> bool:
    """Exercise 2 (LeetCode 125). Two pointers, O(n) time, O(1) extra space."""
    left, right = 0, len(text) - 1
    while left < right:
        if not text[left].isalnum():
            left += 1
        elif not text[right].isalnum():
            right -= 1
        elif text[left].lower() != text[right].lower():
            return False
        else:
            left += 1
            right -= 1
    return True


def move_zeros_to_end(values: list[int]) -> None:
    """Exercise 3 (LeetCode 283): empty shelves to the back, keep the order of the rest. In place, O(n)."""
    write = 0
    for read in range(len(values)):
        if values[read] != 0:
            values[write], values[read] = values[read], values[write]
            write += 1


def squares_sorted(values: list[int]) -> list[int]:
    """Exercise 4 (LeetCode 977): sorted input may contain negatives; biggest squares are at the ENDS."""
    result = [0] * len(values)
    left, right = 0, len(values) - 1
    for position in range(len(values) - 1, -1, -1):
        if abs(values[left]) > abs(values[right]):
            result[position] = values[left] ** 2
            left += 1
        else:
            result[position] = values[right] ** 2
            right -= 1
    return result


def majority_vote(votes: list[str]) -> str | None:
    """Exercise 5 (LeetCode 169 variant): the candidate with MORE than half the votes, if any."""
    counts: dict[str, int] = {}
    for vote in votes:
        counts[vote] = counts.get(vote, 0) + 1
        if counts[vote] > len(votes) // 2:
            return vote
    return None


def longest_streak(days_visited: list[int]) -> int:
    """Exercise 6 (LeetCode 128 idea): longest run of consecutive day numbers, O(n) with a set."""
    days = set(days_visited)
    best = 0
    for day in days:
        if day - 1 not in days:            # only start counting at the beginning of a streak
            length = 1
            while day + length in days:
                length += 1
            best = max(best, length)
    return best


if __name__ == "__main__":
    print(contains_duplicate([4, 1, 7, 1]), is_clean_palindrome("A man, a plan, a canal: Panama"))
    shelf = [0, 3, 0, 5, 8]
    move_zeros_to_end(shelf)
    print(shelf, squares_sorted([-7, -3, 2, 3, 11]))
    print(majority_vote(["cat", "dog", "cat", "cat"]), longest_streak([10, 4, 20, 1, 3, 2, 11]))
