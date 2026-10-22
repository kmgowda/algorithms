"""Volume 5, Chapter 24 - The Fast Fourier Transform: multiplying polynomials and big numbers in O(n log n).

Run:  python3 ch24_examples.py
"""

from __future__ import annotations

import cmath
import random


def schoolbook_poly(a: list, b: list, counter: list | None = None) -> list:
    """Every coefficient of a times every coefficient of b: len(a) x len(b) products."""
    if not a or not b:
        return []
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
            if counter is not None:
                counter[0] += 1
    return out


def evaluate(coeffs: list, x):
    """c0 + c1 x + c2 x^2 + ... (lowest power first), by Horner's rule from the top."""
    total = 0
    for c in reversed(coeffs):
        total = total * x + c
    return total


def roots_of_unity(n: int) -> list:
    """The n points w^0, w^1, ..., w^(n-1) on the unit circle, w = e^(2 pi i / n) (Figure 24.2)."""
    return [cmath.exp(2j * cmath.pi * k / n) for k in range(n)]


def fft(a: list, invert: bool = False, counter: list | None = None) -> list:
    """Values of the polynomial a (length a power of two) at the n-th roots of unity (Figure 24.3)."""
    n = len(a)
    if n == 1:
        return list(a)
    if n & (n - 1):
        raise ValueError("the length must be a power of two")
    even = fft(a[0::2], invert, counter)
    odd = fft(a[1::2], invert, counter)
    sign = -1 if invert else 1
    out = [0] * n
    for k in range(n // 2):
        w = cmath.exp(sign * 2j * cmath.pi * k / n)
        if counter is not None:
            counter[0] += 1
        out[k] = even[k] + w * odd[k]
        out[k + n // 2] = even[k] - w * odd[k]
    return out


def fft_multiply(a: list, b: list, counter: list | None = None) -> list:
    """Product of two integer polynomials: transform, multiply point by point, transform back, round."""
    if not a or not b:
        return []
    size = len(a) + len(b) - 1
    n = 1
    while n < size:
        n *= 2
    fa = fft(list(a) + [0] * (n - len(a)), counter=counter)
    fb = fft(list(b) + [0] * (n - len(b)), counter=counter)
    values = [x * y for x, y in zip(fa, fb)]
    back = fft(values, invert=True, counter=counter)
    return [round((v / n).real) for v in back[:size]]


def digits_low_first(x: int) -> list:
    return [int(d) for d in reversed(str(x))]


def big_multiply(x: int, y: int) -> int:
    """Whole numbers as polynomials in 10: multiply with the FFT, then carry."""
    if x < 0 or y < 0:
        raise ValueError("whole numbers of 0 or more only")
    coeffs = fft_multiply(digits_low_first(x), digits_low_first(y))
    total, carry = 0, 0
    for i, c in enumerate(coeffs):
        carry += c
        total += (carry % 10) * 10 ** i
        carry //= 10
    return total + carry * 10 ** len(coeffs)


def work_table(sizes=(16, 64, 256, 1024, 4096), seed: int = 24) -> list:
    """(n coefficients each, schoolbook products, FFT butterflies) for random polynomials."""
    r = random.Random(seed)
    rows = []
    for n in sizes:
        a = [r.randint(0, 9) for _ in range(n)]
        b = [r.randint(0, 9) for _ in range(n)]
        s, f = [0], [0]
        if n <= 1024:
            schoolbook_poly(a, b, s)
        else:
            s[0] = n * n
        fft_multiply(a, b, f)
        rows.append((n, s[0], f[0]))
    return rows


if __name__ == "__main__":
    print(schoolbook_poly([1, 2, 3], [4, 5]), fft_multiply([1, 2, 3], [4, 5]))
    print(big_multiply(1234, 5678), 1234 * 5678)
    print([round(abs(w), 6) for w in roots_of_unity(4)], [complex(round(w.real, 6), round(w.imag, 6)) for w in roots_of_unity(4)])
    print(work_table())
