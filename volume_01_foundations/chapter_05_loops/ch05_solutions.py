"""Chapter 5 - Solutions to the exercises."""

from __future__ import annotations


def even_numbers_up_to(n: int) -> list[int]:
    """Exercise 1: all even numbers from 2 to n, using range with a step."""
    return list(range(2, n + 1, 2))


def factorial(n: int) -> int:
    """Exercise 2: 5! = 5 x 4 x 3 x 2 x 1 = 120 (the product accumulator)."""
    if n < 0:
        raise ValueError("factorial is not defined for negative numbers")
    product = 1
    for value in range(2, n + 1):
        product *= value
    return product


def count_vowels(text: str) -> int:
    """Exercise 3."""
    count = 0
    for character in text.lower():
        if character in "aeiou":
            count += 1
    return count


def digit_sum(number: int) -> int:
    """Exercise 4: 4096 -> 4 + 0 + 9 + 6 = 19, peeling digits with % and //."""
    number = abs(number)
    total = 0
    while number > 0:
        total += number % 10
        number //= 10
    return total


def fizz_buzz(n: int) -> list[str]:
    """Exercise 5: the classic interview warm-up."""
    out = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            out.append("FizzBuzz")
        elif i % 3 == 0:
            out.append("Fizz")
        elif i % 5 == 0:
            out.append("Buzz")
        else:
            out.append(str(i))
    return out


def triangle(rows: int) -> str:
    """Exercise 6: a star triangle with nested loops."""
    lines = []
    for row in range(1, rows + 1):
        line = ""
        for _ in range(row):
            line += "*"
        lines.append(line)
    return "\n".join(lines)


def days_until_full(capacity_liters: int, rain_per_day: int, evaporation_per_day: int) -> int:
    """Exercise 7: a water tank fills by rain and loses some to evaporation each day."""
    net = rain_per_day - evaporation_per_day
    if net <= 0:
        return -1  # never fills
    water = 0
    days = 0
    while water < capacity_liters:
        water += net
        days += 1
    return days


if __name__ == "__main__":
    print(even_numbers_up_to(10), factorial(5), count_vowels("Elephant"), digit_sum(4096))
    print(fizz_buzz(15))
    print(triangle(4))
    print(days_until_full(100, 15, 5))
