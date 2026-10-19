"""Volume 14, Chapter 5 - Solutions to the exercises."""

from __future__ import annotations

import math


def toy_keys(p: int, q: int, e: int) -> tuple[tuple[int, int], tuple[int, int]]:
    """Exercise 1: build keys by hand from two small primes (e must share no factor with (p-1)(q-1))."""
    phi = (p - 1) * (q - 1)
    if math.gcd(e, phi) != 1:
        raise ValueError("e must be coprime to phi")
    return (e, p * q), (pow(e, -1, phi), p * q)


def crack_small_key(public: tuple[int, int]) -> tuple[int, int]:
    """Exercise 2: with a tiny n, factor it and rebuild the private key - showing why keys must be huge."""
    e, n = public
    p = next(d for d in range(2, math.isqrt(n) + 1) if n % d == 0)
    q = n // p
    return pow(e, -1, (p - 1) * (q - 1)), n


def encrypt_blocks(text: str, public: tuple[int, int]) -> list[int]:
    """Exercise 3: encrypt each character code separately (a toy 'block' scheme - insecure: equal letters
    give equal ciphertexts, which is why real RSA uses random padding)."""
    e, n = public
    return [pow(ord(ch), e, n) for ch in text]


if __name__ == "__main__":
    pub, priv = toy_keys(61, 53, 17)
    print(pub, priv, pow(pow(65, 17, 3233), priv[0], 3233), crack_small_key(pub), encrypt_blocks("aab", pub))
