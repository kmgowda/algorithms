"""Volume 7, Chapter 11 - Big Numbers and Floating Point: what computer numbers can and cannot hold.

Run:  python3 ch11_examples.py
"""

from __future__ import annotations

import math
from fractions import Fraction


def wrap(n: int, bits: int = 8) -> int:
    """What an n-bit signed (two's complement) register holds after storing n (Figure 11.1)."""
    n &= (1 << bits) - 1
    return n - (1 << bits) if n >= 1 << (bits - 1) else n


def add_tenths(times: int) -> float:
    total = 0.0
    for _ in range(times):
        total += 0.1
    return total


def naive_sum(values: list) -> float:
    total = 0.0
    for v in values:
        total += v
    return total


def kahan_sum(values: list) -> float:
    """Compensated summation (Figure 11.3): carry the rounding error forward."""
    total, lost = 0.0, 0.0
    for v in values:
        y = v - lost
        t = total + y
        lost = (t - total) - y
        total = t
    return total


def sys_float_epsilon() -> float:
    import sys
    return sys.float_info.epsilon


def close(a: float, b: float) -> bool:
    return math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-12)


def bits_of(n: int, bits: int = 8) -> str:
    """The bit pattern a two's complement register of the given width stores for n (Figure 11.2)."""
    return format(n & ((1 << bits) - 1), f"0{bits}b")


def negate_pattern(pattern: str) -> str:
    """Two's complement negation: flip every bit, then add 1 (dropping any carry out of the top)."""
    bits = len(pattern)
    flipped = int(pattern, 2) ^ ((1 << bits) - 1)
    return format((flipped + 1) & ((1 << bits) - 1), f"0{bits}b")


def signed_value(pattern: str) -> int:
    """Read a pattern as two's complement: the top bit counts as -2^(w-1)."""
    v = int(pattern, 2)
    return v - (1 << len(pattern)) if pattern[0] == "1" else v


def add_in_register(a: int, b: int, bits: int = 32) -> int:
    """a + b as a fixed-width signed register computes it (wrapping round on overflow)."""
    return wrap(a + b, bits)


def midpoint_unsafe(lo: int, hi: int, bits: int = 32) -> int:
    return wrap(add_in_register(lo, hi, bits) // 2, bits)


def midpoint_safe(lo: int, hi: int) -> int:
    return lo + (hi - lo) // 2


def shift_right_arithmetic(n: int, k: int, bits: int = 8) -> int:
    """Copies the sign bit into the vacated places: -8 >> 1 = -4."""
    return wrap(wrap(n, bits) >> k, bits)


def shift_right_logical(n: int, k: int, bits: int = 8) -> int:
    """Fills with 0s: the pattern of -8 (11111000) shifted right by 1 is 01111100 = 124."""
    return (n & ((1 << bits) - 1)) >> k


def float_parts(x: float) -> tuple[int, int, int]:
    """(sign bit, stored exponent, 52-bit fraction) of a 64-bit IEEE 754 double (Figure 11.4)."""
    import struct
    raw = struct.unpack(">Q", struct.pack(">d", x))[0]
    return raw >> 63, (raw >> 52) & 0x7FF, raw & ((1 << 52) - 1)


def float_value_from_parts(sign: int, exponent: int, fraction: int) -> float:
    """Rebuild a normal double: (-1)^sign x (1 + fraction / 2^52) x 2^(exponent - 1023)."""
    return (-1) ** sign * (1 + Fraction(fraction, 1 << 52)) * Fraction(2) ** (exponent - 1023)


def one_minus_cos_naive(x: float) -> float:
    return (1 - math.cos(x)) / (x * x)


def one_minus_cos_stable(x: float) -> float:
    """The same quantity rewritten to avoid subtracting nearly equal numbers: 2 sin^2(x/2) / x^2."""
    return 2 * math.sin(x / 2) ** 2 / (x * x)


def small_root_naive(b: float, c: float) -> float:
    """Smaller root of x^2 - b x + c = 0 by the school formula (b - sqrt(b^2 - 4c)) / 2: cancellation when b^2 >> c."""
    return (b - math.sqrt(b * b - 4 * c)) / 2


def small_root_stable(b: float, c: float) -> float:
    """The same root as c / (larger root): no subtraction of nearly equal numbers."""
    return c / ((b + math.sqrt(b * b - 4 * c)) / 2)


def kahan_trace(values: list) -> list:
    """Kahan summation with its trace: rows (value, corrected y, new total, lost)."""
    total, lost, rows = 0.0, 0.0, []
    for v in values:
        y = v - lost
        t = total + y
        lost = (t - total) - y
        total = t
        rows.append((v, y, total, lost))
    return rows


if __name__ == "__main__":
    print(wrap(127), wrap(128), wrap(200), wrap(-1), wrap(300), 2 ** 100)
    print(0.1 + 0.2, 0.1 + 0.2 == 0.3, close(0.1 + 0.2, 0.3), add_tenths(10), add_tenths(10) == 1.0)
    big = [1e16] + [1.0] * 10000
    print(naive_sum(big) - 1e16, kahan_sum(big) - 1e16, math.fsum(big) - 1e16)
    print(2.0 ** 53 + 1 == 2.0 ** 53, Fraction(1, 10) + Fraction(2, 10) == Fraction(3, 10), 1e308 * 10, float("inf") - float("inf"))
    print(bits_of(5), bits_of(-5), negate_pattern("00000101"), signed_value("11111011"), bits_of(-128), negate_pattern("10000000"))
    print(add_in_register(2 ** 31 - 1, 1), midpoint_unsafe(2 ** 30 + 5, 2 ** 31 - 3), midpoint_safe(2 ** 30 + 5, 2 ** 31 - 3))
    print(shift_right_arithmetic(-8, 1), shift_right_logical(-8, 1), bits_of(-8))
    for x in (1.0, 0.1, -2.5, 2.0 ** -1074, float("inf")):
        print(x, float_parts(x))
    print(float(float_value_from_parts(*float_parts(0.1))), Fraction(0.1), math.ulp(1.0), 2 ** -52, math.ulp(1e6), math.ulp(1e16))
    print(one_minus_cos_naive(1e-8), one_minus_cos_stable(1e-8), one_minus_cos_naive(1e-4), one_minus_cos_stable(1e-4))
    print(small_root_naive(1e8, 1.0), small_root_stable(1e8, 1.0))
    print(kahan_trace([1e16, 1.0, 1.0, 1.0, 1.0]), naive_sum([1e16, 1.0, 1.0, 1.0, 1.0]) - 1e16)
    print(float("nan") == float("nan"), 0.1 + 0.2 - 0.3, sys_float_epsilon())
