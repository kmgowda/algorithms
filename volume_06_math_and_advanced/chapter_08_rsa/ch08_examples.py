"""Volume 6, Chapter 8 - Secret Messages: RSA in Miniature (a teaching toy, never for real secrets).

Run:  python3 ch08_examples.py
"""

from __future__ import annotations

import math


def make_keys(p: int, q: int, e: int = 17) -> tuple[tuple, tuple]:
    """Public key (n, e) and private key (n, d) from two primes (Figure 8.2)."""
    n, phi = p * q, (p - 1) * (q - 1)
    if math.gcd(e, phi) != 1:
        raise ValueError("e must share no factor with (p - 1)(q - 1)")
    d = pow(e, -1, phi)                               # the inverse of Chapter 4
    return (n, e), (n, d)


def encrypt(m: int, public: tuple) -> int:
    n, e = public
    if not 0 <= m < n:
        raise ValueError("the message number must be at least 0 and below n")
    return pow(m, e, n)


def decrypt(c: int, private: tuple) -> int:
    n, d = private
    return pow(c, d, n)


def text_to_numbers(text: str) -> list:
    return [ord(ch) for ch in text]


def factor_by_trial(n: int) -> tuple[int, int] | None:
    """What an eavesdropper must do: factor n. Easy here, hopeless for 600-digit n."""
    d = 2
    while d * d <= n:
        if n % d == 0:
            return d, n // d
        d += 1
    return None


if __name__ == "__main__":
    public, private = make_keys(61, 53)
    print(public, private)
    c = encrypt(65, public)
    print(c, decrypt(c, private))
    msg = text_to_numbers("MEET AT 9")
    code = [encrypt(m, public) for m in msg]
    print(code, "".join(chr(decrypt(x, private)) for x in code))
    print(factor_by_trial(3233), encrypt(0, public), encrypt(1, public))
