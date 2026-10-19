"""Volume 14, Chapter 1 - Bits and Bytes: How Numbers Live Inside Computers.

Run:  python3 ch01_examples.py
"""

from __future__ import annotations

import math
import struct


def to_binary(n: int, width: int = 8) -> str:
    """Write a non-negative integer in binary, padded to `width` bits, by repeated division by 2."""
    bits = []
    for _ in range(width):
        bits.append(str(n % 2))
        n //= 2
    return "".join(reversed(bits))


def from_binary(bits: str) -> int:
    """Read binary back: each step doubles the value and adds the next bit (Horner's rule)."""
    value = 0
    for b in bits:
        value = value * 2 + int(b)
    return value


def twos_complement(n: int, width: int = 8) -> str:
    """How a fixed-width machine stores a signed integer: negative n is stored as 2^width + n."""
    return to_binary(n % (1 << width), width)


def wrap_signed(n: int, width: int = 32) -> int:
    """Simulate a fixed-width signed integer (like int32 in C or Java): values wrap around on overflow."""
    n %= 1 << width
    return n - (1 << width) if n >= 1 << (width - 1) else n


def float_bits(x: float) -> str:
    """The 64 bits of an IEEE 754 double: 1 sign bit, 11 exponent bits, 52 fraction bits."""
    raw = struct.unpack(">Q", struct.pack(">d", x))[0]
    b = to_binary(raw, 64)
    return f"{b[0]} {b[1:12]} {b[12:]}"


def close_enough(a: float, b: float) -> bool:
    """Compare decimals with a tolerance instead of ==."""
    return math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-12)


def money_in_cents(prices: list[str]) -> int:
    """Industry example: store money as whole cents (integers) so sums are exact."""
    total = 0
    for p in prices:
        rupees, _, paise = p.partition(".")
        total += int(rupees) * 100 + int((paise + "00")[:2])
    return total


if __name__ == "__main__":
    print(to_binary(13), from_binary("00001101"), twos_complement(-13), twos_complement(-1))
    print("int32 overflow:", wrap_signed(2_147_483_647 + 1), "| 2**31 - 1 + 1 in Python:", 2_147_483_647 + 1)
    print("0.1 + 0.2 =", 0.1 + 0.2, "| == 0.3?", 0.1 + 0.2 == 0.3, "| close?", close_enough(0.1 + 0.2, 0.3))
    print("bits of 0.1:", float_bits(0.1))
    print("sum of 0.1 ten times:", sum([0.1] * 10), "| in cents:", money_in_cents(["0.10"] * 10), "paise")
