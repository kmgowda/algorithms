"""Volume 4, Chapter 21 - Fast Multiplication: Karatsuba's three half-size products instead of four.

Run:  python3 ch21_examples.py
"""

from __future__ import annotations


def school(x: int, y: int, counter: list) -> int:
    """Schoolbook long multiplication: every digit of x times every digit of y (Figure 21.1)."""
    xs, ys = [int(d) for d in str(x)][::-1], [int(d) for d in str(y)][::-1]
    total = 0
    for i, a in enumerate(xs):
        for j, b in enumerate(ys):
            counter[0] += 1
            total += a * b * 10 ** (i + j)
    return total


def split_four(x: int, y: int, counter: list) -> int:
    """Divide and conquer with four half-size products: no faster than school (Figure 21.2)."""
    if x < 10 or y < 10:
        counter[0] += 1
        return x * y
    m = max(len(str(x)), len(str(y))) // 2
    a, b = divmod(x, 10 ** m)
    c, d = divmod(y, 10 ** m)
    ac, ad, bc, bd = (split_four(a, c, counter), split_four(a, d, counter), split_four(b, c, counter),
                      split_four(b, d, counter))
    return ac * 10 ** (2 * m) + (ad + bc) * 10 ** m + bd


def karatsuba(x: int, y: int, counter: list) -> int:
    """Karatsuba (Figure 21.3): ad + bc = (a + b)(c + d) - ac - bd, so three products are enough."""
    if x < 0 or y < 0:
        raise ValueError("whole numbers of 0 or more only")
    if x < 10 or y < 10:
        counter[0] += 1
        return x * y
    m = max(len(str(x)), len(str(y))) // 2
    a, b = divmod(x, 10 ** m)
    c, d = divmod(y, 10 ** m)
    ac = karatsuba(a, c, counter)
    bd = karatsuba(b, d, counter)
    middle = karatsuba(a + b, c + d, counter) - ac - bd
    return ac * 10 ** (2 * m) + middle * 10 ** m + bd


if __name__ == "__main__":
    for x, y in ((1234, 5678), (12345678, 87654321)):
        c1, c2, c3 = [0], [0], [0]
        print(x * y, school(x, y, c1), split_four(x, y, c2), karatsuba(x, y, c3), c1[0], c2[0], c3[0])
