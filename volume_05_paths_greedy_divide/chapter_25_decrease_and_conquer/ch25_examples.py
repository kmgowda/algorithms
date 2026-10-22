"""Volume 5, Chapter 25 - Decrease and Conquer: shrink the problem by one, by half, or by a variable amount.

Run:  python3 ch25_examples.py
"""

from __future__ import annotations


def power(x: int, n: int, counter: list) -> int:
    """x to the n by halving n (Figure 25.2): about 2 log2 n multiplications instead of n - 1."""
    if n < 0:
        raise ValueError("the power must be 0 or more")
    if n == 0:
        return 1
    half = power(x, n // 2, counter)
    counter[0] += 1
    result = half * half
    if n % 2:
        counter[0] += 1
        result *= x
    return result


def peasant(a: int, b: int, log: list | None = None) -> int:
    """Russian peasant multiplication (Figure 25.3): halve a, double b, add b whenever a is odd."""
    total = 0
    while a > 0:
        if log is not None:
            log.append((a, b, a % 2 == 1))
        if a % 2:
            total += b
        a, b = a // 2, b * 2
    return total


def guess_number(secret: int, low: int, high: int) -> int:
    """Guess a number in low..high by halving the range each time; returns the number of guesses."""
    guesses = 0
    while low <= high:
        guesses += 1
        mid = (low + high) // 2
        if mid == secret:
            return guesses
        if mid < secret:
            low = mid + 1
        else:
            high = mid - 1
    return guesses


def euclid(a: int, b: int, log: list | None = None) -> int:
    """Greatest common divisor: replace (a, b) by (b, a mod b); the size shrinks by a varying amount."""
    while b:
        if log is not None:
            log.append((a, b))
        a, b = b, a % b
    return a


def power_steps(n: int) -> list:
    """The exponents built by Power on the way back up (Figure 25.2), smallest first, e.g. 13 -> [1, 3, 6, 13]."""
    steps = []
    while n:
        steps.append(n)
        n //= 2
    return steps[::-1]


def insertion_sort_rec(values: list, counter: list) -> list:
    """Decrease by one: sort all but the last value, then insert the last (T(n) = T(n - 1) + n)."""
    if len(values) <= 1:
        return list(values)
    out = insertion_sort_rec(values[:-1], counter)
    v, i = values[-1], len(out)
    while i > 0:
        counter[0] += 1
        if out[i - 1] <= v:
            break
        i -= 1
    return out[:i] + [v] + out[i:]


def josephus_order(n: int) -> list:
    """Section 25.5: readers 1..n sit in a circle; going round, every second reader leaves. The order they leave."""
    circle, out, i = list(range(1, n + 1)), [], 1
    while len(circle) > 1:
        i %= len(circle)
        out.append(circle.pop(i))
        i += 1
    return out + circle


def josephus(n: int) -> int:
    """The last reader left, by the halving recurrence J(1) = 1, J(2k) = 2J(k) - 1, J(2k + 1) = 2J(k) + 1."""
    if n < 1:
        raise ValueError("at least one reader")
    if n == 1:
        return 1
    return 2 * josephus(n // 2) - 1 if n % 2 == 0 else 2 * josephus(n // 2) + 1


def josephus_bits(n: int) -> int:
    """The same answer by moving the leading 1 bit of n to the end: 10 = 1010 -> 0101 = 5."""
    b = bin(n)[2:]
    return int(b[1:] + b[0], 2)


if __name__ == "__main__":
    c = [0]
    print(power(3, 13, c), c[0], 3 ** 13)
    log = []
    print(peasant(13, 21, log), log)
    print(max(guess_number(s, 1, 1000) for s in range(1, 1001)))
    log = []
    print(euclid(1071, 462, log), log)
