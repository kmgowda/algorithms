"""Volume 1, Chapter 2, Thinking Problem 2 - adding two binary numbers digit by digit.

The school method for addition, in base 2: start at the rightmost bits, add the two bits and the carry,
write the remainder (mod 2) and carry the rest (div 2). One step per bit position, plus a final carry.

Run:  python3 ch02_solutions.py
"""

from __future__ import annotations


def add_binary(x: str, y: str) -> str:
    """Add two binary strings (empty means 0); the answer has no leading zeros, except "0" itself."""
    i, j, carry = len(x) - 1, len(y) - 1, 0
    digits = ""
    while i >= 0 or j >= 0 or carry > 0:
        s = carry
        if i >= 0:
            s += int(x[i])
            i -= 1
        if j >= 0:
            s += int(y[j])
            j -= 1
        digits = str(s % 2) + digits
        carry = s // 2
    digits = digits.lstrip("0")
    return digits if digits else "0"


if __name__ == "__main__":
    print(add_binary("1001101", "11001"), add_binary("11111111", "1"), add_binary("", ""))
