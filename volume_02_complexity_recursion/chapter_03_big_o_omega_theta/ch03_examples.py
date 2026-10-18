"""Volume 2, Chapter 3 - Big O, Big Omega, Big Theta: Upper, Lower, and Tight Bounds.

The functions here CHECK bound claims numerically over a range of n.
A numeric check is evidence, not a proof - the chapter shows the proofs.

Run:  python3 ch03_examples.py
"""

from __future__ import annotations

from typing import Callable

Fn = Callable[[int], float]


def exact_steps_report_card(students: int) -> int:
    """T(n) for a report job: 3 setup steps, then 5 steps per student, then 2 steps to finish."""
    return 3 + 5 * students + 2


def exact_steps_pairs(n: int) -> int:
    """T(n) for comparing every pair once: n(n-1)/2 comparisons."""
    return n * (n - 1) // 2


def is_upper_bound(f: Fn, g: Fn, c: float, n0: int, check_up_to: int = 10_000) -> bool:
    """Big O witness check: f(n) <= c * g(n) for every n from n0 to check_up_to."""
    return all(f(n) <= c * g(n) for n in range(n0, check_up_to + 1))


def is_lower_bound(f: Fn, g: Fn, c: float, n0: int, check_up_to: int = 10_000) -> bool:
    """Big Omega witness check: f(n) >= c * g(n) for every n from n0 to check_up_to."""
    return all(f(n) >= c * g(n) for n in range(n0, check_up_to + 1))


def is_tight_bound(f: Fn, g: Fn, c_low: float, c_high: float, n0: int, check_up_to: int = 10_000) -> bool:
    """Big Theta witness check: c_low * g(n) <= f(n) <= c_high * g(n) from n0 on."""
    return (is_lower_bound(f, g, c_low, n0, check_up_to)
            and is_upper_bound(f, g, c_high, n0, check_up_to))


def find_upper_witness(f: Fn, g: Fn, check_up_to: int = 2_000) -> tuple[int, int] | None:
    """Search small whole-number (c, n0) pairs that make f = O(g) true over the checked range."""
    for c in range(1, 101):
        for n0 in (1, 2, 5, 10, 50, 100, 500):
            if is_upper_bound(f, g, c, n0, check_up_to):
                return c, n0
    return None


def ratio_trend(f: Fn, g: Fn, sizes: tuple[int, ...] = (10, 100, 1_000, 10_000, 100_000)) -> list[float]:
    """f(n)/g(n) at growing n.

    Ratio settles to a positive constant -> Theta(g).
    Ratio shrinks toward 0               -> f = O(g) but not Theta (f grows strictly slower: little-o).
    Ratio grows without limit            -> f is not O(g).
    """
    return [f(n) / g(n) for n in sizes]


def dominant_term(coefficients: dict[int, float]) -> int:
    """For a polynomial given as {power: coefficient}, the power that decides its Theta class."""
    powers = [power for power, coefficient in coefficients.items() if coefficient != 0]
    if not powers:
        raise ValueError("zero polynomial")
    return max(powers)


def delivery_window(distance_km: float) -> tuple[float, float]:
    """Industry example: a promise with a lower AND upper bound, like Theta.

    At least 10 minutes of cooking + 2 min/km; at most 20 minutes + 4 min/km.
    """
    return 10 + 2 * distance_km, 20 + 4 * distance_km


if __name__ == "__main__":
    n_squared: Fn = lambda n: n * n
    linear: Fn = lambda n: n
    print("T(n) = 5n + 5 is O(n) with c=6, n0=5:", is_upper_bound(exact_steps_report_card, linear, 6, 5))
    print("T(n) = 5n + 5 is Omega(n) with c=5, n0=1:", is_lower_bound(exact_steps_report_card, linear, 5, 1))
    print("pairs is Theta(n^2) with 1/4 and 1/2, n0=2:", is_tight_bound(exact_steps_pairs, n_squared, 0.25, 0.5, 2))
    print("Witness for 3n^2 + 10n = O(n^2):", find_upper_witness(lambda n: 3 * n * n + 10 * n, n_squared))
    print("Ratio n / n^2:", ratio_trend(linear, n_squared))
    print("Ratio pairs / n^2:", [round(r, 4) for r in ratio_trend(exact_steps_pairs, n_squared)])
    print("Dominant power of 7n^3 + 2n + 9:", dominant_term({3: 7, 1: 2, 0: 9}))
    print("Delivery window for 5 km:", delivery_window(5))
