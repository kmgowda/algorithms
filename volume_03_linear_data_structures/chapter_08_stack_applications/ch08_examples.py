"""Volume 3, Chapter 8 - Stack Applications: Expression Evaluation and Monotonic Stacks.

Run:  python3 ch08_examples.py
"""

from __future__ import annotations

PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2}


def tokenize(expression: str) -> list[str]:
    """Split '12+3*(4-1)' into ['12', '+', '3', '*', '(', '4', '-', '1', ')']."""
    tokens: list[str] = []
    number = ""
    for ch in expression:
        if ch.isdigit() or ch == ".":
            number += ch
            continue
        if number:
            tokens.append(number)
            number = ""
        if ch in "+-*/()":
            tokens.append(ch)
        elif not ch.isspace():
            raise ValueError(f"unexpected character {ch!r}")
    if number:
        tokens.append(number)
    return tokens


def evaluate_postfix(tokens: list[str]) -> float:
    """'3 4 + 2 *' means (3 + 4) * 2. Numbers are pushed; an operator pops two and pushes the result."""
    stack: list[float] = []
    for token in tokens:
        if token in PRECEDENCE:
            if len(stack) < 2:
                raise ValueError("not enough numbers for operator " + token)
            right, left = stack.pop(), stack.pop()
            if token == "+":
                stack.append(left + right)
            elif token == "-":
                stack.append(left - right)
            elif token == "*":
                stack.append(left * right)
            else:
                stack.append(left / right)
        else:
            stack.append(float(token))
    if len(stack) != 1:
        raise ValueError("malformed expression")
    return stack[0]


def infix_to_postfix(tokens: list[str]) -> list[str]:
    """Dijkstra's shunting-yard algorithm: operators wait on a stack until something weaker arrives."""
    output: list[str] = []
    operators: list[str] = []
    for token in tokens:
        if token in PRECEDENCE:
            while operators and operators[-1] != "(" and PRECEDENCE[operators[-1]] >= PRECEDENCE[token]:
                output.append(operators.pop())
            operators.append(token)
        elif token == "(":
            operators.append(token)
        elif token == ")":
            while operators and operators[-1] != "(":
                output.append(operators.pop())
            if not operators:
                raise ValueError("unbalanced parentheses")
            operators.pop()                      # discard the "("
        else:
            output.append(token)
    while operators:
        if operators[-1] == "(":
            raise ValueError("unbalanced parentheses")
        output.append(operators.pop())
    return output


def calculate(expression: str) -> float:
    """Industry example: a calculator app = tokenize -> shunting yard -> postfix evaluation."""
    return evaluate_postfix(infix_to_postfix(tokenize(expression)))


# ------------------------------------------------------------------ monotonic stacks
def next_greater(values: list[int]) -> list[int]:
    """For each item, the next item to its right that is bigger (-1 if none). O(n) total.

    The stack holds indexes whose answer is still unknown, with values in DECREASING order.
    """
    answer = [-1] * len(values)
    waiting: list[int] = []
    for i, value in enumerate(values):
        while waiting and values[waiting[-1]] < value:
            answer[waiting.pop()] = value
        waiting.append(i)
    return answer


def days_until_warmer(temperatures: list[int]) -> list[int]:
    """LeetCode 739: practical example - how many days until a warmer day?"""
    answer = [0] * len(temperatures)
    waiting: list[int] = []
    for day, temp in enumerate(temperatures):
        while waiting and temperatures[waiting[-1]] < temp:
            earlier = waiting.pop()
            answer[earlier] = day - earlier
        waiting.append(day)
    return answer


def stock_span(prices: list[int]) -> list[int]:
    """Industry example (LeetCode 901): for each day, how many consecutive days up to today had price <= today's?"""
    spans: list[int] = []
    stack: list[tuple[int, int]] = []          # (price, span) with prices strictly decreasing
    for price in prices:
        span = 1
        while stack and stack[-1][0] <= price:
            span += stack.pop()[1]
        stack.append((price, span))
        spans.append(span)
    return spans


if __name__ == "__main__":
    print(tokenize("12 + 3*(4-1)"))
    print(infix_to_postfix(tokenize("12 + 3*(4-1)")), "=", calculate("12 + 3*(4-1)"))
    print("(2+3)*4 - 10/5 =", calculate("(2+3)*4 - 10/5"))
    print("Next greater:", next_greater([4, 5, 2, 25, 7, 3]))
    print("Days until warmer:", days_until_warmer([30, 32, 31, 29, 33, 28, 35]))
    print("Stock span:", stock_span([100, 80, 60, 70, 60, 75, 85]))
