"""Volume 14, Chapter 1 - Solutions to the exercises."""

from __future__ import annotations

from ch01_examples import wrap_signed


def reverse_integer(x: int) -> int:
    """Exercise 1 (LeetCode 7): reverse the digits; return 0 if the result does not fit in a signed 32-bit int."""
    sign = -1 if x < 0 else 1
    r = sign * int(str(abs(x))[::-1])
    return r if wrap_signed(r) == r else 0


def to_base(n: int, base: int) -> str:
    """Exercise 2: write n in any base from 2 to 16."""
    digits = "0123456789ABCDEF"
    if n == 0:
        return "0"
    out = []
    while n:
        out.append(digits[n % base])
        n //= base
    return "".join(reversed(out))


def add_binary(a: str, b: str) -> str:
    """Exercise 3 (LeetCode 67): add two binary strings digit by digit with a carry, as the hardware does."""
    out, carry = [], 0
    i, j = len(a) - 1, len(b) - 1
    while i >= 0 or j >= 0 or carry:
        total = carry + (int(a[i]) if i >= 0 else 0) + (int(b[j]) if j >= 0 else 0)
        out.append(str(total % 2))
        carry = total // 2
        i, j = i - 1, j - 1
    return "".join(reversed(out)) or "0"


if __name__ == "__main__":
    print(reverse_integer(123), reverse_integer(-120), reverse_integer(1534236469), to_base(255, 16), add_binary("1011", "11"))
