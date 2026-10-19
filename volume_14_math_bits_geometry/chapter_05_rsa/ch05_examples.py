"""Volume 14, Chapter 5 - Cryptography Intuition: RSA.

A TOY implementation for learning. Real systems use vetted libraries, 2048+ bit keys and padding schemes.

Run:  python3 ch05_examples.py
"""

from __future__ import annotations

import math
import random
import time


def is_probable_prime(n: int, rounds: int = 20, rng: random.Random | None = None) -> bool:
    """Miller-Rabin test: a composite number fails for at least 3/4 of the random bases, so 20 rounds make a
    wrong 'prime' answer less likely than 1 in 10^12."""
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29):
        if n % p == 0:
            return n == p
    rng = rng or random.Random(0)
    d, s = n - 1, 0
    while d % 2 == 0:
        d, s = d // 2, s + 1
    for _ in range(rounds):
        x = pow(rng.randrange(2, n - 1), d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def random_prime(bits: int, rng: random.Random) -> int:
    """Pick random odd numbers with the top bit set until one is (probably) prime."""
    while True:
        candidate = rng.getrandbits(bits) | 1 << (bits - 1) | 1
        if is_probable_prime(candidate, rng=rng):
            return candidate


def make_keys(bits: int = 64, e: int = 65537, seed: int = 1) -> tuple[tuple[int, int], tuple[int, int]]:
    """RSA key generation: n = p*q, phi = (p-1)(q-1), d = inverse of e mod phi.
    Public key (e, n), private key (d, n)."""
    rng = random.Random(seed)
    while True:
        p, q = random_prime(bits // 2, rng), random_prime(bits // 2, rng)
        phi = (p - 1) * (q - 1)
        if p != q and math.gcd(e, phi) == 1:
            break
    d = pow(e, -1, phi)
    return (e, p * q), (d, p * q)


def encrypt(message: int, public: tuple[int, int]) -> int:
    e, n = public
    return pow(message, e, n)


def decrypt(cipher: int, private: tuple[int, int]) -> int:
    d, n = private
    return pow(cipher, d, n)


def text_to_int(text: str) -> int:
    return int.from_bytes(text.encode("utf-8"), "big")


def int_to_text(value: int) -> str:
    return value.to_bytes((value.bit_length() + 7) // 8, "big").decode("utf-8")


def sign(message: int, private: tuple[int, int]) -> int:
    """Industry example: a digital signature is 'encryption' with the private key; anyone can check it."""
    return pow(message, private[0], private[1])


def verify(message: int, signature: int, public: tuple[int, int]) -> bool:
    return pow(signature, public[0], public[1]) == message


def factor_time(n: int) -> tuple[int, float]:
    """Why RSA is safe: recovering p from n by trial division gets slower very quickly as n grows."""
    start = time.perf_counter()
    d = 3 if n % 2 else 2
    while n % d:
        d += 2
    return d, time.perf_counter() - start


if __name__ == "__main__":
    public, private = make_keys(64)
    msg = text_to_int("Hi!")
    c = encrypt(msg, public)
    print("public", public, "| cipher", c, "| decrypted", int_to_text(decrypt(c, private)))
    s = sign(msg, private)
    print("signature valid:", verify(msg, s, public), "| tampered:", verify(msg + 1, s, public))
    for bits in (24, 32, 40, 48):
        pub, _ = make_keys(bits, seed=bits)
        p, secs = factor_time(pub[1])
        print(f"{bits}-bit n: factor {p} found in {secs * 1000:.1f} ms")
