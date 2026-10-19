"""Volume 14, Chapter 8 - Matrices and Fast Fourier Transform (Intuition).

Run:  python3 ch08_examples.py
"""

from __future__ import annotations

import cmath
import random
import timeit

Matrix = list[list[int]]


def mat_mul(a: Matrix, b: Matrix, mod: int | None = None) -> Matrix:
    """Row-times-column multiplication: O(n^3) for n x n matrices."""
    n, m, p = len(a), len(b), len(b[0])
    out = [[0] * p for _ in range(n)]
    for i in range(n):
        for k in range(m):
            if a[i][k]:
                for j in range(p):
                    out[i][j] += a[i][k] * b[k][j]
        if mod:
            out[i] = [x % mod for x in out[i]]
    return out


def mat_pow(a: Matrix, e: int, mod: int | None = None) -> Matrix:
    """Fast power for matrices (Chapter 4's repeated squaring): O(n^3 log e)."""
    n = len(a)
    result = [[int(i == j) for j in range(n)] for i in range(n)]
    while e:
        if e & 1:
            result = mat_mul(result, a, mod)
        a = mat_mul(a, a, mod)
        e >>= 1
    return result


def fibonacci_matrix(n: int, mod: int | None = None) -> int:
    """[[1, 1], [1, 0]]^n = [[F(n+1), F(n)], [F(n), F(n-1)]] - the n-th Fibonacci number in O(log n) steps."""
    return mat_pow([[1, 1], [1, 0]], n, mod)[0][1]


def poly_mul_naive(a: list[int], b: list[int]) -> list[int]:
    """Multiply polynomials (coefficient lists, lowest power first) the school way: O(n x m)."""
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def fft(values: list[complex], invert: bool = False) -> list[complex]:
    """Recursive FFT (divide and conquer, V10): evaluate a polynomial at the n complex n-th roots of unity
    by splitting into even and odd coefficients. n must be a power of two. O(n log n)."""
    n = len(values)
    if n == 1:
        return list(values)
    even, odd = fft(values[0::2], invert), fft(values[1::2], invert)
    sign = -1 if invert else 1
    out = [0j] * n
    for k in range(n // 2):
        w = cmath.exp(sign * 2j * cmath.pi * k / n) * odd[k]
        out[k], out[k + n // 2] = even[k] + w, even[k] - w
    return out


def poly_mul_fft(a: list[int], b: list[int]) -> list[int]:
    """Evaluate both at the roots of unity, multiply pointwise, interpolate back with the inverse FFT."""
    size = 1
    while size < len(a) + len(b) - 1:
        size *= 2
    fa = fft([complex(x) for x in a] + [0j] * (size - len(a)))
    fb = fft([complex(x) for x in b] + [0j] * (size - len(b)))
    product = fft([x * y for x, y in zip(fa, fb)], invert=True)
    return [round(v.real / size) for v in product[:len(a) + len(b) - 1]]


def race(n: int, seed: int = 0) -> dict[str, float]:
    rng = random.Random(seed)
    a = [rng.randint(0, 9) for _ in range(n)]
    b = [rng.randint(0, 9) for _ in range(n)]
    return {"naive": min(timeit.repeat(lambda: poly_mul_naive(a, b), number=1, repeat=3)),
            "FFT": min(timeit.repeat(lambda: poly_mul_fft(a, b), number=1, repeat=3))}


def big_multiply(x: int, y: int) -> int:
    """Industry example: multiply huge integers by treating their digits as polynomial coefficients (x = 10)."""
    a = [int(d) for d in str(x)[::-1]]
    b = [int(d) for d in str(y)[::-1]]
    coeffs = poly_mul_fft(a, b)
    return sum(c * 10 ** i for i, c in enumerate(coeffs))


if __name__ == "__main__":
    print(mat_mul([[1, 2], [3, 4]], [[5, 6], [7, 8]]), [fibonacci_matrix(n) for n in range(10)])
    print("F(10^18) mod 10^9+7:", fibonacci_matrix(10 ** 18, 1_000_000_007))
    print(poly_mul_naive([1, 2], [3, 4]), poly_mul_fft([1, 2], [3, 4]))
    for n in (256, 1024, 4096):
        r = race(n)
        print(f"degree {n}: naive {r['naive'] * 1000:.1f} ms, FFT {r['FFT'] * 1000:.1f} ms")
    print(big_multiply(12345678901234567890, 98765432109876543210) == 12345678901234567890 * 98765432109876543210)
