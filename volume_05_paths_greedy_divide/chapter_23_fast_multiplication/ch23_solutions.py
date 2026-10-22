"""Volume 5, Chapter 23 - Thinking Problems.

Problem 1: when no split ever carries, n = 2^k digits need exactly 3^k single-digit products (checked on 11...1).
Problem 2: squaring with three half-size squarings: (a 10^m + b)^2 = a^2 10^2m + ((a + b)^2 - a^2 - b^2) 10^m + b^2.
Problem 3: "Karatsuba is always faster": on small numbers it does more digit work; find where it starts to win.
"""

from __future__ import annotations



def karatsuba_square(x: int, counter: list) -> int:
    if x < 0:
        raise ValueError("whole numbers of 0 or more only")
    if x < 10:
        counter[0] += 1
        return x * x
    m = len(str(x)) // 2
    a, b = divmod(x, 10 ** m)
    a2, b2 = karatsuba_square(a, counter), karatsuba_square(b, counter)
    middle = karatsuba_square(a + b, counter) - a2 - b2       # 2ab
    return a2 * 10 ** (2 * m) + middle * 10 ** m + b2


def first_winning_size(threshold: int = 1) -> int | None:
    """The first size in ops_table where Karatsuba (with this threshold) uses fewer digit operations."""
    from ch23_examples import ops_table
    col = 2 if threshold == 1 else 3
    return next((row[0] for row in ops_table(threshold=max(threshold, 2) if threshold > 1 else 32) if row[col] < row[1]), None)


if __name__ == "__main__":
    c = [0]
    print(karatsuba_square(12345678, c), 12345678 ** 2, c[0], first_winning_size(1), first_winning_size(32))
