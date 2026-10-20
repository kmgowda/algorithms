"""Volume 1, Chapter 12 - The Math Toolkit.

Run:  python3 ch12_examples.py
"""

from __future__ import annotations


def gauss_sum(n: int) -> int:
    """1 + 2 + ... + n = n(n + 1) / 2 (Figure 12.1)."""
    return n * (n + 1) // 2


def powers_of_two_sum(k: int) -> int:
    """1 + 2 + 4 + ... + 2^(k-1) = 2^k - 1 (Figure 12.2)."""
    return 2 ** k - 1


def halving_total(start: int) -> int:
    """start + start//2 + start//4 + ... down to 1: less than 2 * start (Figure 12.4)."""
    total = 0
    while start >= 1:
        total += start
        start //= 2
    return total


def check_formulas(n: int) -> bool:
    """Compare the toolkit's formulas with direct sums for one n >= 1 (Figures 12.1, 12.2 and 12.5)."""
    gauss = sum(range(1, n + 1)) == n * (n + 1) // 2
    powers = sum(2 ** i for i in range(n)) == 2 ** n - 1
    halvings, m = 0, n
    while m > 1:
        m //= 2
        halvings += 1
    return gauss and powers and halvings == n.bit_length() - 1      # floor(log2 n)


if __name__ == "__main__":
    print(gauss_sum(10), gauss_sum(100), powers_of_two_sum(5), powers_of_two_sum(10), halving_total(1000))
    print(all(check_formulas(n) for n in range(1, 500)))
