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
    """Divide and conquer with four half-size products: no faster than school (Section 21.4)."""
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
    """Karatsuba (Figures 21.2 and 21.3): ad + bc = (a + b)(c + d) - ac - bd, so three products are enough."""
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


def karatsuba_calls(x: int, y: int) -> tuple:
    """The call tree of Karatsuba (Figure 21.3): (x, y, [children]) with leaves for single-digit factors."""
    if x < 10 or y < 10:
        return (x, y, [])
    m = max(len(str(x)), len(str(y))) // 2
    a, b = divmod(x, 10 ** m)
    c, d = divmod(y, 10 ** m)
    return (x, y, [karatsuba_calls(a, c), karatsuba_calls(b, d), karatsuba_calls(a + b, c + d)])


def digits(v: int) -> int:
    return len(str(abs(v)))


def school_ops(x: int, y: int) -> int:
    """Digit operations of long multiplication: one product and about one addition for each pair of digits."""
    return 2 * digits(x) * digits(y)


def karatsuba_ops(x: int, y: int, threshold: int = 1) -> int:
    """Digit operations of Karatsuba (Section 21.7): single-digit products at the bottom, plus the digits of every
    addition and subtraction made by the splits. Below `threshold` digits it switches to the schoolbook method."""
    if x < 10 or y < 10 or max(digits(x), digits(y)) < threshold:
        return school_ops(x, y) if threshold > 1 else 1
    m = max(digits(x), digits(y)) // 2
    a, b = divmod(x, 10 ** m)
    c, d = divmod(y, 10 ** m)
    ac, bd, s = a * c, b * d, (a + b) * (c + d)
    ops = karatsuba_ops(a, c, threshold) + karatsuba_ops(b, d, threshold) + karatsuba_ops(a + b, c + d, threshold)
    ops += digits(a) + digits(b) + digits(c) + digits(d)      # forming a + b and c + d
    ops += 2 * digits(s)                                       # subtracting ac and bd from the middle product
    ops += 2 * digits(x * y)                                   # adding the three shifted pieces
    return ops


def ops_table(sizes=(16, 32, 64, 128, 256, 512, 1024), seed: int = 3, threshold: int = 32) -> list:
    """Figure 21.7: (digits, schoolbook ops, pure Karatsuba ops, Karatsuba with schoolbook below `threshold`)."""
    import random
    rng = random.Random(seed)
    out = []
    for n in sizes:
        x, y = rng.randrange(10 ** (n - 1), 10 ** n), rng.randrange(10 ** (n - 1), 10 ** n)
        out.append((n, school_ops(x, y), karatsuba_ops(x, y), karatsuba_ops(x, y, threshold)))
    return out


def strassen(A: list, B: list, counter: list) -> list:
    """Strassen's seven products for square matrices whose size is a power of two (Section 21.5, Figure 21.5).
    counter[0] counts scalar multiplications."""
    n = len(A)
    if n == 1:
        counter[0] += 1
        return [[A[0][0] * B[0][0]]]
    h = n // 2

    def block(M, r, c):
        return [row[c * h:(c + 1) * h] for row in M[r * h:(r + 1) * h]]

    def add(P, Q):
        return [[p + q for p, q in zip(rp, rq)] for rp, rq in zip(P, Q)]

    def sub(P, Q):
        return [[p - q for p, q in zip(rp, rq)] for rp, rq in zip(P, Q)]

    a, b, c, d = block(A, 0, 0), block(A, 0, 1), block(A, 1, 0), block(A, 1, 1)
    e, f, g, k = block(B, 0, 0), block(B, 0, 1), block(B, 1, 0), block(B, 1, 1)
    p1 = strassen(a, sub(f, k), counter)
    p2 = strassen(add(a, b), k, counter)
    p3 = strassen(add(c, d), e, counter)
    p4 = strassen(d, sub(g, e), counter)
    p5 = strassen(add(a, d), add(e, k), counter)
    p6 = strassen(sub(b, d), add(g, k), counter)
    p7 = strassen(sub(a, c), add(e, f), counter)
    top_left = add(sub(add(p5, p4), p2), p6)
    top_right = add(p1, p2)
    bottom_left = add(p3, p4)
    bottom_right = sub(sub(add(p5, p1), p3), p7)
    top = [l + r for l, r in zip(top_left, top_right)]
    bottom = [l + r for l, r in zip(bottom_left, bottom_right)]
    return top + bottom


def matrix_school(A: list, B: list, counter: list) -> list:
    """Row-times-column multiplication: n^3 scalar multiplications."""
    n = len(A)
    out = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for t in range(n):
                counter[0] += 1
                out[i][j] += A[i][t] * B[t][j]
    return out


if __name__ == "__main__":
    for x, y in ((1234, 5678), (12345678, 87654321)):
        c1, c2, c3 = [0], [0], [0]
        print(x * y, school(x, y, c1), split_four(x, y, c2), karatsuba(x, y, c3), c1[0], c2[0], c3[0])
