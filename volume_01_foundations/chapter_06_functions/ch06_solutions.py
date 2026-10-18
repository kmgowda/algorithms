"""Chapter 6 - Solutions to the exercises."""

from __future__ import annotations


def square(number: float) -> float:
    """Exercise 1."""
    return number * number


def is_adult(age: int, adult_age: int = 18) -> bool:
    """Exercise 2: a default parameter lets different countries change the rule."""
    return age >= adult_age


def kilometers_to_miles(km: float) -> float:
    """Exercise 3."""
    return km * 0.621371


def bmi(weight_kg: float, height_m: float) -> float:
    """Exercise 4: body-mass index, rounded to 1 decimal place."""
    if height_m <= 0:
        raise ValueError("height must be positive")
    return round(weight_kg / (height_m * height_m), 1)


def bmi_category(value: float) -> str:
    if value < 18.5:
        return "underweight"
    if value < 25:
        return "healthy"
    if value < 30:
        return "overweight"
    return "obese"


def describe_bmi(weight_kg: float, height_m: float) -> str:
    """Exercise 4: composes two smaller functions."""
    value = bmi(weight_kg, height_m)
    return f"BMI {value} ({bmi_category(value)})"


def count_multiples(limit: int, divisor: int) -> int:
    """Exercise 5: how many numbers from 1 to limit are divisible by divisor?"""
    count = 0
    for number in range(1, limit + 1):
        if number % divisor == 0:
            count += 1
    return count


def bus_trip_cost(stops: int, price_per_stop: float = 5.0, max_price: float = 40.0) -> float:
    """Exercise 6: price grows with stops but is capped."""
    return min(stops * price_per_stop, max_price)


def is_prime(n: int) -> bool:
    """Exercise 7: a number > 1 whose only divisors are 1 and itself."""
    if n < 2:
        return False
    divisor = 2
    while divisor * divisor <= n:     # no need to check beyond the square root
        if n % divisor == 0:
            return False
        divisor += 1
    return True


def base_fee(days_late: int, per_day: float = 2.0) -> float:
    return max(days_late, 0) * per_day

def member_discount(fee: float, is_member: bool) -> float:
    return fee / 2 if is_member else fee

def late_fee(days_late: int, is_member: bool) -> float:
    return member_discount(base_fee(days_late), is_member)


if __name__ == "__main__":
    print(square(7), is_adult(17), kilometers_to_miles(10), late_fee(5, True))
    print(describe_bmi(70, 1.75))
    print(count_multiples(100, 7), bus_trip_cost(12))
    print([n for n in range(30) if is_prime(n)])
