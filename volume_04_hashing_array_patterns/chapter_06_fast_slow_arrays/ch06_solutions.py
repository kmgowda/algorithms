"""Volume 4, Chapter 6 - Solutions to the exercises."""

from __future__ import annotations

from ch06_examples import digit_square_sum, find_cycle


def is_happy_with_set(n: int) -> bool:
    """Exercise 1: the visited-set version - simpler, but O(cycle) memory."""
    seen: set[int] = set()
    while n != 1 and n not in seen:
        seen.add(n)
        n = digit_square_sum(n)
    return n == 1


def circular_loop(jumps: list[int]) -> bool:
    """Exercise 2 (LeetCode 457): from each index jump jumps[i] steps around a circle.
    Is there a loop longer than 1 that keeps one direction? Fast/slow from each start."""
    n = len(jumps)

    def nxt(i: int) -> int:
        return (i + jumps[i]) % n

    for start in range(n):
        forward = jumps[start] > 0

        def same_direction(i: int) -> bool:
            return (jumps[i] > 0) == forward

        slow = fast = start
        while same_direction(fast) and same_direction(nxt(fast)):
            slow, fast = nxt(slow), nxt(nxt(fast))
            if slow == fast:
                if nxt(slow) != slow:          # a loop of length 1 doesn't count
                    return True
                break
    return False


def gift_chain_length(gives_to: list[int], start: int) -> int:
    """Exercise 3: in a secret-gift game, person i gives to gives_to[i]. How many people are in start's loop?"""
    _, length = find_cycle(start, lambda i: gives_to[i])
    return length


if __name__ == "__main__":
    print(is_happy_with_set(7), circular_loop([2, -1, 1, 2, 2]), circular_loop([-1, 2]), gift_chain_length([1, 2, 0, 4, 3], 0))
