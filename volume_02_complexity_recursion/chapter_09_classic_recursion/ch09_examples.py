"""Volume 2, Chapter 9 - Recursion III: Classic Problems.

Run:  python3 ch09_examples.py
"""

from __future__ import annotations

from functools import lru_cache
from typing import Any


# ------------------------------------------------------------------ fast power
def power_slow(base: int, exponent: int) -> tuple[int, int]:
    """b^e = b x b^(e-1): e multiplications. Returns (answer, multiplications)."""
    if exponent == 0:
        return 1, 0
    rest, mults = power_slow(base, exponent - 1)
    return base * rest, mults + 1


def power_fast(base: int, exponent: int) -> tuple[int, int]:
    """Exponentiation by squaring: b^e = (b^(e/2))^2, times b if e is odd. About 2 log2(e) multiplications."""
    if exponent == 0:
        return 1, 0
    half, mults = power_fast(base, exponent // 2)
    result = half * half
    mults += 1
    if exponent % 2 == 1:
        result *= base
        mults += 1
    return result, mults


def power_mod(base: int, exponent: int, modulus: int) -> int:
    """Industry example: (b^e) mod m, the core of RSA encryption, without ever building b^e."""
    if exponent == 0:
        return 1 % modulus
    half = power_mod(base, exponent // 2, modulus)
    result = (half * half) % modulus
    if exponent % 2 == 1:
        result = (result * base) % modulus
    return result


# ------------------------------------------------------------------ Euclid's GCD
def gcd(a: int, b: int) -> int:
    """Greatest common divisor: gcd(a, b) = gcd(b, a mod b), and gcd(a, 0) = a."""
    if b == 0:
        return abs(a)
    return gcd(b, a % b)


def gcd_steps(a: int, b: int) -> list[tuple[int, int]]:
    """The pairs Euclid's algorithm visits, to show how quickly they shrink."""
    steps = [(a, b)]
    while b:
        a, b = b, a % b
        steps.append((a, b))
    return steps


def aspect_ratio(width: int, height: int) -> str:
    """Industry example: simplify a screen size like 1920 x 1080 to 16:9."""
    divisor = gcd(width, height)
    return f"{width // divisor}:{height // divisor}"


# ------------------------------------------------------------------ Fibonacci, fixed with memoization
def fibonacci_memo(n: int, memo: dict[int, int] | None = None) -> int:
    """Remember every answer the first time it is computed; reuse it afterwards. O(n) calls."""
    if memo is None:
        memo = {}
    if n < 2:
        return n
    if n not in memo:
        memo[n] = fibonacci_memo(n - 1, memo) + fibonacci_memo(n - 2, memo)
    return memo[n]


@lru_cache(maxsize=None)
def fibonacci_cached(n: int) -> int:
    """The same idea using Python's built-in memoization decorator."""
    if n < 2:
        return n
    return fibonacci_cached(n - 1) + fibonacci_cached(n - 2)


def memo_call_count(n: int) -> int:
    """Count the calls made by the memoized version (compare with Chapter 8's naive count)."""
    calls = 0
    memo: dict[int, int] = {}

    def fib(k: int) -> int:
        nonlocal calls
        calls += 1
        if k < 2:
            return k
        if k not in memo:
            memo[k] = fib(k - 1) + fib(k - 2)
        return memo[k]

    fib(n)
    return calls


# ------------------------------------------------------------------ Tower of Hanoi
def hanoi(disks: int, source: str = "A", spare: str = "B", target: str = "C") -> list[tuple[int, str, str]]:
    """Move `disks` disks from source to target. Each move is (disk, from, to). 2^n - 1 moves."""
    if disks == 0:
        return []
    moves = hanoi(disks - 1, source, target, spare)       # move the smaller tower out of the way
    moves.append((disks, source, target))                   # move the biggest disk
    moves += hanoi(disks - 1, spare, source, target)       # move the smaller tower on top of it
    return moves


def hanoi_is_valid(disks: int, moves: list[tuple[int, str, str]]) -> bool:
    """Replay the moves and check no bigger disk is ever placed on a smaller one."""
    pegs = {"A": list(range(disks, 0, -1)), "B": [], "C": []}
    for disk, source, target in moves:
        if not pegs[source] or pegs[source][-1] != disk:
            return False
        if pegs[target] and pegs[target][-1] < disk:
            return False
        pegs[target].append(pegs[source].pop())
    return pegs["C"] == list(range(disks, 0, -1))


# ------------------------------------------------------------------ flattening nested data
def flatten(items: list[Any]) -> list[Any]:
    """[1, [2, [3, 4]], 5] -> [1, 2, 3, 4, 5]."""
    result: list[Any] = []
    for item in items:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def all_products(category: dict[str, Any]) -> list[str]:
    """Industry example: an online shop's category tree; list every product under a category."""
    products = list(category.get("products", []))
    for sub in category.get("subcategories", []):
        products.extend(all_products(sub))
    return products


SHOP: dict[str, Any] = {
    "name": "Electronics",
    "products": [],
    "subcategories": [
        {"name": "Phones", "products": ["Phone X", "Phone Y"], "subcategories": []},
        {"name": "Audio", "products": ["Speaker"], "subcategories": [
            {"name": "Headphones", "products": ["Buds", "Over-ear"], "subcategories": []},
        ]},
    ],
}


if __name__ == "__main__":
    print("2^30 slow vs fast (answer, multiplications):", power_slow(2, 30), power_fast(2, 30))
    print("7^560 mod 561:", power_mod(7, 560, 561), "| pow():", pow(7, 560, 561))
    print("gcd(1071, 462):", gcd(1071, 462), gcd_steps(1071, 462))
    print("1920x1080 is", aspect_ratio(1920, 1080), "| 2560x1600 is", aspect_ratio(2560, 1600))
    print("F(90):", fibonacci_memo(90), fibonacci_cached(90), "| memo calls for F(30):", memo_call_count(30))
    moves = hanoi(3)
    print("Hanoi with 3 disks:", len(moves), "moves", moves, "valid:", hanoi_is_valid(3, moves))
    print("Flatten:", flatten([1, [2, [3, 4]], 5, [[[6]]]]))
    print("Products under Electronics:", all_products(SHOP))
