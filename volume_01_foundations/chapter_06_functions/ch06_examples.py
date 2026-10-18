"""Chapter 6 - Functions: Reusable Recipes.

Run:  python3 ch06_examples.py
"""

from __future__ import annotations


# ---------------------------------------------------------------- beginner example
def boil_water(cups: int) -> str:
    """A small recipe reused by bigger recipes."""
    return f"boil {cups} cup(s) of water"


def make_tea(cups: int) -> list[str]:
    return [boil_water(cups), f"add {cups} tea bag(s)", "wait 3 minutes"]


def boil_egg(eggs: int) -> list[str]:
    return [boil_water(2), f"put {eggs} egg(s) in", "wait 9 minutes"]


# ---------------------------------------------------------------- parameters and defaults
def greet(name: str, greeting: str = "Hello") -> str:
    """`greeting` has a default value, so callers may leave it out."""
    return f"{greeting}, {name}!"


# ---------------------------------------------------------------- practical examples
def rectangle_area(length: float, width: float) -> float:
    return length * width


def circle_area(radius: float) -> float:
    pi = 3.141592653589793
    return pi * radius * radius


def paint_cans_needed(wall_length: float, wall_height: float, coverage_per_can: float = 10.0) -> int:
    """Practical example: a school repaints a wall. Builds on rectangle_area and rounds up."""
    area = rectangle_area(wall_length, wall_height)
    cans = area / coverage_per_can
    whole_cans = int(cans)
    if cans > whole_cans:          # any leftover area needs one more can
        whole_cans += 1
    return whole_cans


def average(total: float, count: int) -> float:
    if count == 0:
        raise ValueError("cannot average zero items")
    return total / count


def report_card_line(name: str, maths: int, science: int, english: int) -> str:
    """Practical example: functions calling functions to build a report."""
    mean = average(maths + science + english, 3)
    return f"{name}: average {mean:.1f}, {'PASS' if mean >= 40 else 'FAIL'}"


# ---------------------------------------------------------------- industry examples
def is_valid_amount(amount: float) -> bool:
    return amount > 0


def has_enough_money(balance: float, amount: float) -> bool:
    return balance >= amount


def transfer(from_balance: float, to_balance: float, amount: float) -> tuple[float, float, str]:
    """Industry example: a bank transfer built from small, testable functions."""
    if not is_valid_amount(amount):
        return from_balance, to_balance, "Rejected: amount must be positive"
    if not has_enough_money(from_balance, amount):
        return from_balance, to_balance, "Rejected: insufficient funds"
    return from_balance - amount, to_balance + amount, "Success"


def apply_coupon(price: float, coupon: str) -> float:
    coupons = {"SAVE10": 0.10, "HALF": 0.50}
    return price * (1 - coupons.get(coupon, 0.0))


def add_delivery(price: float, free_above: float = 500.0, fee: float = 40.0) -> float:
    return price if price > free_above else price + fee


def checkout_price(price: float, coupon: str = "") -> float:
    """Industry example: an online shop's price pipeline (one function per rule)."""
    return round(add_delivery(apply_coupon(price, coupon)), 2)


# ---------------------------------------------------------------- scope
zoo_name = "City Zoo"            # a global variable: visible everywhere in this file


def describe_scope() -> str:
    visitors = 120               # a local variable: exists only while this function runs
    return f"{zoo_name} had {visitors} visitors"


# ---------------------------------------------------------------- pure function vs side effect
def add_points_pure(score: int, points: int) -> int:
    """Pure: same inputs always give the same output, and nothing else changes."""
    return score + points


game_log: list[str] = []


def add_points_with_log(score: int, points: int) -> int:
    """Has a side effect: it also changes something outside itself (the log)."""
    game_log.append(f"+{points}")
    return score + points


if __name__ == "__main__":
    print(make_tea(2))
    print(boil_egg(3))
    print(greet("Maya"), greet("Leo", greeting="Good morning"))
    print("Paint cans:", paint_cans_needed(12, 3))
    print(report_card_line("Aisha", 78, 85, 69))
    print(transfer(1000, 200, 300))
    print("Checkout:", checkout_price(450, "SAVE10"))
    print(describe_scope())
