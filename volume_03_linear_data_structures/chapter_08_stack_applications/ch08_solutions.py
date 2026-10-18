"""Volume 3, Chapter 8 - Solutions to the exercises."""

from __future__ import annotations


def evaluate_rpn(tokens: list[str]) -> int:
    """Exercise 1 (LeetCode 150): integer postfix where division truncates toward zero."""
    stack: list[int] = []
    for token in tokens:
        if token in {"+", "-", "*", "/"}:
            b, a = stack.pop(), stack.pop()
            if token == "+":
                stack.append(a + b)
            elif token == "-":
                stack.append(a - b)
            elif token == "*":
                stack.append(a * b)
            else:
                stack.append(int(a / b))
        else:
            stack.append(int(token))
    return stack[0]


def previous_smaller(values: list[int]) -> list[int]:
    """Exercise 2: the nearest item to the LEFT that is smaller (-1 if none)."""
    answer: list[int] = []
    stack: list[int] = []                     # values in increasing order
    for value in values:
        while stack and stack[-1] >= value:
            stack.pop()
        answer.append(stack[-1] if stack else -1)
        stack.append(value)
    return answer


def largest_rectangle(heights: list[int]) -> int:
    """Exercise 3 (LeetCode 84): the biggest rectangle under a skyline of bars. O(n) with a monotonic stack."""
    best = 0
    stack: list[int] = []                     # indexes with increasing heights
    for i, h in enumerate(heights + [0]):     # a final 0 flushes the stack
        while stack and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            left = stack[-1] + 1 if stack else 0
            best = max(best, height * (i - left))
        stack.append(i)
    return best


def remove_k_digits(number: str, k: int) -> str:
    """Exercise 4 (LeetCode 402): delete k digits to make the smallest number. Greedy + increasing stack."""
    stack: list[str] = []
    for digit in number:
        while k and stack and stack[-1] > digit:
            stack.pop()
            k -= 1
        stack.append(digit)
    if k:
        stack = stack[:-k]
    result = "".join(stack).lstrip("0")
    return result or "0"


if __name__ == "__main__":
    print(evaluate_rpn(["2", "1", "+", "3", "*"]), previous_smaller([4, 5, 2, 10, 8]))
    print(largest_rectangle([2, 1, 5, 6, 2, 3]), remove_k_digits("1432219", 3))
