"""Volume 7, Chapter 8 - Secret Messages: RSA in Miniature (a teaching toy, never for real secrets).

Run:  python3 ch08_examples.py
"""

from __future__ import annotations

import math


def make_keys(p: int, q: int, e: int = 17) -> tuple[tuple, tuple]:
    """Public key (n, e) and private key (n, d) from two primes (Section 8.4)."""
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


def decrypt_crt(c: int, p: int, q: int, d: int) -> tuple[int, dict]:
    """Decrypt with the remainder theorem (Figure 8.4): two half-size powers mod p and mod q, then combine.
    Returns (message, the intermediate values)."""
    dp, dq = d % (p - 1), d % (q - 1)             # Fermat shortens the exponents
    m1, m2 = pow(c, dp, p), pow(c, dq, q)
    q_inv = pow(q, -1, p)
    h = q_inv * (m1 - m2) % p
    m = m2 + h * q
    return m, {"dp": dp, "dq": dq, "m1": m1, "m2": m2, "q_inv": q_inv, "h": h}


def factor_from_phi(n: int, phi: int) -> tuple[int, int] | None:
    """Knowing phi = (p - 1)(q - 1) gives p + q = n - phi + 1, so p and q are the roots of x^2 - (p + q) x + n."""
    s = n - phi + 1
    disc = s * s - 4 * n
    if disc < 0:
        return None
    r = math.isqrt(disc)
    if r * r != disc:
        return None
    p, q = (s - r) // 2, (s + r) // 2
    return (p, q) if p * q == n else None


def integer_cube_root(x: int) -> int:
    lo, hi = 0, 1 << ((x.bit_length() + 2) // 3 + 1)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid ** 3 <= x:
            lo = mid
        else:
            hi = mid - 1
    return lo


def fermat_factor(n: int, max_steps: int = 10 ** 6) -> tuple[int, int, int] | None:
    """Fermat's method: search a >= sqrt(n) with a^2 - n a perfect square b^2, so n = (a - b)(a + b). Returns (p, q, steps)."""
    a = math.isqrt(n)
    if a * a < n:
        a += 1
    for step in range(1, max_steps + 1):
        b2 = a * a - n
        b = math.isqrt(b2)
        if b * b == b2:
            return a - b, a + b, step
        a += 1
    return None


def bits_of_work(exponent: int) -> int:
    return exponent.bit_length()


def diffie_hellman(p: int, g: int, a: int, b: int) -> tuple[int, int, int, int]:
    """Two people agree a secret over an open line: Maya sends A = g^a mod p, Leo sends B = g^b mod p, and each
    raises what they receive to their own secret. Returns (A, B, Maya's key B^a, Leo's key A^b)."""
    A, B = pow(g, a, p), pow(g, b, p)
    return A, B, pow(B, a, p), pow(A, b, p)


def discrete_log_brute(g: int, h: int, p: int) -> tuple[int | None, int]:
    """The eavesdropper's problem: find x with g^x = h (mod p) by trying x = 0, 1, 2, ... Returns (x, tries)."""
    v = 1
    for x in range(p - 1):
        if v == h:
            return x, x + 1
        v = v * g % p
    return None, p - 1


def baby_step_giant_step(g: int, h: int, p: int) -> tuple[int | None, int]:
    """Shanks: write x = i m + j with m about sqrt(p); store g^j for every j, then step h * g^(-m) i times.
    About 2 sqrt(p) multiplications instead of p. Returns (x, multiplications)."""
    import math
    m = math.isqrt(p - 1) + 1
    table, v = {}, 1
    for j in range(m):
        table.setdefault(v, j)
        v = v * g % p
    step = pow(g, -m, p)
    y, work = h, m
    for i in range(m):
        if y in table:
            return i * m + table[y], work + i
        y = y * step % p
    return None, work + m


if __name__ == "__main__":
    public, private = make_keys(61, 53)
    print(public, private)
    c = encrypt(65, public)
    print(c, decrypt(c, private))
    msg = text_to_numbers("MEET AT 9")
    code = [encrypt(m, public) for m in msg]
    print(code, "".join(chr(decrypt(x, private)) for x in code))
    print(factor_by_trial(3233), encrypt(0, public), encrypt(1, public))
    print(decrypt_crt(2790, 61, 53, 2753), all(decrypt_crt(encrypt(m, public), 61, 53, 2753)[0] == m for m in range(3233)))
    print(factor_from_phi(3233, 3120), encrypt(61, public), decrypt(encrypt(61, public), private), encrypt(106, public))
    pub3, priv3 = make_keys(1019, 1031, 3)
    c3 = encrypt(97, pub3)
    print(pub3, c3, 97 ** 3, integer_cube_root(c3))
    print(encrypt(2, public) * encrypt(65, public) % 3233, encrypt(130, public))
    print(fermat_factor(3233), fermat_factor(1019 * 1031), bits_of_work(2753), bits_of_work(53), bits_of_work(49))
    print(diffie_hellman(23, 5, 6, 15), discrete_log_brute(5, 8, 23), baby_step_giant_step(5, 8, 23))
