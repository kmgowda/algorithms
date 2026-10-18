"""Volume 2, Chapter 6 - Solutions to the exercises."""

from __future__ import annotations

from ch06_examples import arithmetic_sum, ceil_log2, geometric_sum


def seats_in_theater(first_row: int, extra_per_row: int, rows: int) -> int:
    """Exercise 1: row 1 has first_row seats, each later row has extra_per_row more."""
    last_row = first_row + (rows - 1) * extra_per_row
    return arithmetic_sum(first_row, last_row, rows)


def nested_loop_steps(n: int) -> int:
    """Exercise 2: for i in range(n): for j in range(i): one step -> 0 + 1 + ... + (n-1)."""
    return arithmetic_sum(0, n - 1, n) if n > 0 else 0


def savings_plan(monthly: float, months: int, growth: float) -> float:
    """Exercise 3: save `monthly`, increasing the amount by `growth` (e.g. 1.05) each month."""
    return round(geometric_sum(monthly, growth, months), 2)


def phone_book_halvings(names: int) -> int:
    """Exercise 4: worst-case pages opened by repeatedly halving a phone book."""
    return ceil_log2(names + 1)


def simplify_log_expression() -> dict[str, float]:
    """Exercise 5: log rules, checked numerically with base-2 logs at x = 64, y = 8."""
    import math
    x, y = 64, 8
    return {
        "log(x*y) = log x + log y": math.log2(x * y) - (math.log2(x) + math.log2(y)),
        "log(x/y) = log x - log y": math.log2(x / y) - (math.log2(x) - math.log2(y)),
        "log(x^3) = 3 log x": math.log2(x ** 3) - 3 * math.log2(x),
    }


def levels_for_items(items: int, branching: int) -> int:
    """Exercise 6: levels needed so a tree with `branching` children per node holds `items` leaves."""
    levels, capacity = 0, 1
    while capacity < items:
        capacity *= branching
        levels += 1
    return levels


if __name__ == "__main__":
    print(seats_in_theater(20, 2, 15), nested_loop_steps(10), savings_plan(100, 12, 1.05))
    print(phone_book_halvings(1_000_000), simplify_log_expression(), levels_for_items(1_000_000, 100))
