"""Volume 10, Chapter 9 - Fast Multiplication: Karatsuba and Strassen.

Numbers are lists of decimal digits, least significant first, so we control every digit operation
(Python's own int multiplication already uses Karatsuba internally for big numbers).

Run:  python3 ch09_examples.py
"""

from __future__ import annotations

import random
import timeit

Digits = list[int]


def to_digits(n: int) -> Digits:
    return [int(c) for c in reversed(str(n))] or [0]


def from_digits(d: Digits) -> int:
    return int("".join(map(str, reversed(d))) or "0")


def add(a: Digits, b: Digits) -> Digits:
    out, carry = [], 0
    for i in range(max(len(a), len(b))):
        s = (a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) + carry
        out.append(s % 10)
        carry = s // 10
    if carry:
        out.append(carry)
    return out


def subtract(a: Digits, b: Digits) -> Digits:
    """a - b for a >= b."""
    out, borrow = [], 0
    for i in range(len(a)):
        s = a[i] - (b[i] if i < len(b) else 0) - borrow
        borrow = 1 if s < 0 else 0
        out.append(s + 10 if s < 0 else s)
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def shift(a: Digits, k: int) -> Digits:
    """Multiply by 10^k: put k zeros at the low end."""
    return [0] * k + a if a != [0] else [0]


def schoolbook(a: Digits, b: Digits) -> Digits:
    """The method taught in school: every digit times every digit. O(n^2) digit multiplications."""
    out = [0] * (len(a) + len(b))
    for i, x in enumerate(a):
        carry = 0
        for j, y in enumerate(b):
            cur = out[i + j] + x * y + carry
            out[i + j] = cur % 10
            carry = cur // 10
        k = i + len(b)
        while carry:
            cur = out[k] + carry
            out[k] = cur % 10
            carry = cur // 10
            k += 1
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def karatsuba(a: Digits, b: Digits, cutoff: int = 32) -> Digits:
    """Split each number into high and low halves: a = a1*10^m + a0, b = b1*10^m + b0.
    Three multiplications instead of four: a1*b1, a0*b0, and (a1+a0)(b1+b0) - the middle term is the
    third minus the first two. T(n) = 3T(n/2) + O(n) = O(n^1.585). Small inputs use schoolbook."""
    if min(len(a), len(b)) <= cutoff:
        return schoolbook(a, b)
    m = max(len(a), len(b)) // 2
    a0, a1 = a[:m] or [0], a[m:] or [0]
    b0, b1 = b[:m] or [0], b[m:] or [0]
    high = karatsuba(a1, b1, cutoff)
    low = karatsuba(a0, b0, cutoff)
    middle = subtract(subtract(karatsuba(add(a1, a0), add(b1, b0), cutoff), high), low)
    return add(add(shift(high, 2 * m), shift(middle, m)), low)


Matrix = list[list[int]]


def mat_mult(A: Matrix, B: Matrix) -> Matrix:
    """Ordinary matrix multiplication: n^3 multiplications."""
    n, m, p = len(A), len(B), len(B[0])
    return [[sum(A[i][k] * B[k][j] for k in range(m)) for j in range(p)] for i in range(n)]


def strassen(A: Matrix, B: Matrix, cutoff: int = 32) -> Matrix:
    """Square matrices with size a power of two. 7 half-size products instead of 8: T(n) = 7T(n/2) + O(n^2) = O(n^2.807)."""
    n = len(A)
    if n <= cutoff:
        return mat_mult(A, B)
    h = n // 2

    def split(M: Matrix) -> tuple[Matrix, Matrix, Matrix, Matrix]:
        return ([r[:h] for r in M[:h]], [r[h:] for r in M[:h]], [r[:h] for r in M[h:]], [r[h:] for r in M[h:]])

    def plus(X: Matrix, Y: Matrix) -> Matrix:
        return [[x + y for x, y in zip(rx, ry)] for rx, ry in zip(X, Y)]

    def minus(X: Matrix, Y: Matrix) -> Matrix:
        return [[x - y for x, y in zip(rx, ry)] for rx, ry in zip(X, Y)]

    a, b, c, d = split(A)
    e, f, g, k = split(B)
    p1 = strassen(a, minus(f, k), cutoff)
    p2 = strassen(plus(a, b), k, cutoff)
    p3 = strassen(plus(c, d), e, cutoff)
    p4 = strassen(d, minus(g, e), cutoff)
    p5 = strassen(plus(a, d), plus(e, k), cutoff)
    p6 = strassen(minus(b, d), plus(g, k), cutoff)
    p7 = strassen(minus(a, c), plus(e, f), cutoff)
    top_left = plus(minus(plus(p5, p4), p2), p6)
    top_right = plus(p1, p2)
    bottom_left = plus(p3, p4)
    bottom_right = minus(minus(plus(p1, p5), p3), p7)
    return [l + r for l, r in zip(top_left, top_right)] + [l + r for l, r in zip(bottom_left, bottom_right)]


def race_multiplication(digits: int, seed: int = 0) -> dict[str, float]:
    """Time schoolbook vs Karatsuba on two random numbers with the given number of digits."""
    rng = random.Random(seed)
    a = [rng.randint(0, 9) for _ in range(digits - 1)] + [rng.randint(1, 9)]
    b = [rng.randint(0, 9) for _ in range(digits - 1)] + [rng.randint(1, 9)]
    return {"schoolbook": min(timeit.repeat(lambda: schoolbook(a, b), number=1, repeat=3)),
            "karatsuba": min(timeit.repeat(lambda: karatsuba(a, b), number=1, repeat=3))}


if __name__ == "__main__":
    x, y = 31415926535897932384, 27182818284590452353
    print(from_digits(karatsuba(to_digits(x), to_digits(y), cutoff=2)) == x * y)
    for n in (100, 400, 1600):
        print(n, "digits:", {k: round(v, 4) for k, v in race_multiplication(n).items()})
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    print(strassen(A, B, cutoff=1), mat_mult(A, B))
