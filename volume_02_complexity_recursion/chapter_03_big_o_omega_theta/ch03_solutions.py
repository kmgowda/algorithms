"""Volume 2, Chapter 3 - Solutions to the exercises."""

from __future__ import annotations

import math

from ch03_examples import find_upper_witness, is_lower_bound, is_tight_bound, is_upper_bound


def exercise2_witness() -> tuple[int, int]:
    """Exercise 2: 4n + 7 <= 5n once n >= 7, so c = 5, n0 = 7 proves 4n + 7 = O(n)."""
    c, n0 = 5, 7
    assert is_upper_bound(lambda n: 4 * n + 7, lambda n: n, c, n0)
    return c, n0


def exercise3_theta() -> tuple[float, float, int]:
    """Exercise 3: n^2/2 + 3n is between (1/2) n^2 and 1 * n^2 once n >= 6."""
    c_low, c_high, n0 = 0.5, 1.0, 6
    assert is_tight_bound(lambda n: n * n / 2 + 3 * n, lambda n: n * n, c_low, c_high, n0)
    return c_low, c_high, n0


def is_n_squared_big_o_of_n() -> bool:
    """Exercise 4: no constant works - find_upper_witness fails to find one."""
    return find_upper_witness(lambda n: n * n, lambda n: n) is not None


def log_vs_sqrt_lower_bound() -> bool:
    """Exercise 5: sqrt(n) >= log2(n) once n >= 16, so sqrt(n) = Omega(log n)."""
    return is_lower_bound(lambda n: math.sqrt(n), lambda n: math.log2(n), 1, 16, 100_000)


def classify_claims() -> dict[str, bool]:
    """Exercise 6: which statements are TRUE?"""
    return {
        "n = O(n^2)": True,          # an upper bound may be loose
        "n^2 = O(n)": False,
        "n = Omega(n^2)": False,
        "n^2 = Omega(n)": True,
        "3n + 2 = Theta(n)": True,
        "n log n = Theta(n)": False,  # n log n grows strictly faster than n
    }


if __name__ == "__main__":
    print(exercise2_witness(), exercise3_theta(), is_n_squared_big_o_of_n(), log_vs_sqrt_lower_bound())
    print(classify_claims())
