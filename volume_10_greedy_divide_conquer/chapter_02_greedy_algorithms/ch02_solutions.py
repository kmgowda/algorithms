"""Volume 10, Chapter 2 - Solutions to the exercises."""

from __future__ import annotations


def min_jumps(jumps: list[int]) -> int:
    """Exercise 1 (LeetCode 45): fewest jumps to the last stone - greedy by 'levels' of reach (like BFS)."""
    count, current_end, farthest = 0, 0, 0
    for i in range(len(jumps) - 1):
        farthest = max(farthest, i + jumps[i])
        if i == current_end:
            count += 1
            current_end = farthest
    return count


def max_profit_many_trades(prices: list[int]) -> int:
    """Exercise 2 (LeetCode 122): buy and sell any number of times - take every rising day."""
    return sum(max(0, b - a) for a, b in zip(prices, prices[1:]))


def smallest_after_removing(digits: list[int], k: int) -> str:
    """Exercise 3 (LeetCode 402 idea): remove k digits to keep the SMALLEST number - drop a digit when a smaller one follows."""
    stack: list[int] = []
    for d in digits:
        while k and stack and stack[-1] > d:
            stack.pop()
            k -= 1
        stack.append(d)
    stack = stack[:len(stack) - k] if k else stack
    return "".join(map(str, stack)).lstrip("0") or "0"


def lemonade_change(bills: list[int]) -> bool:
    """Exercise 4 (LeetCode 860): sell 5-rupee lemonade; give change from 5s and 10s - use a 10 first when paid 20."""
    fives = tens = 0
    for b in bills:
        if b == 5:
            fives += 1
        elif b == 10:
            if not fives:
                return False
            fives, tens = fives - 1, tens + 1
        elif tens and fives:
            tens, fives = tens - 1, fives - 1
        elif fives >= 3:
            fives -= 3
        else:
            return False
    return True


if __name__ == "__main__":
    print(min_jumps([2, 3, 1, 1, 4]), max_profit_many_trades([7, 1, 5, 3, 6, 4]),
          smallest_after_removing([1, 4, 3, 2, 2, 1, 9], 3), lemonade_change([5, 5, 5, 10, 20]))
