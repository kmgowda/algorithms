"""Chapter 6, Section 6.11: every way to test a prime, side by side. Counts the basic steps each method needs for
primes of growing size, and shows which methods a Carmichael number fools."""
import os
import sys
from math import isqrt

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(folder: str, module: str):
    """Load a sibling chapter's module from its file under a unique name: module names repeat across volumes
    (every volume has a ch06_examples), so a plain import could pick up the wrong one."""
    import importlib.util
    path = os.path.join(HERE, "..", folder, module + ".py")
    spec = importlib.util.spec_from_file_location(f"{os.path.basename(os.path.dirname(HERE))}.{folder}.{module}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

c06 = _load("chapter_06_testing_primes", "ch06_examples")

DIGITS = [4, 6, 8, 10, 12, 16, 20, 30]


def trial_divisions(n: int) -> int:
    """Divisions made by ch06_examples.trial when n is prime: every d from 2 to the square root of n."""
    return max(isqrt(n) - 1, 0)


def trial_divisions_counted(n: int) -> int:
    """The same count, by running the loop (for checking the formula on small n)."""
    d, count = 2, 0
    while d * d <= n:
        count += 1
        if n % d == 0:
            break
        d += 1
    return count


def power_mults(e: int) -> int:
    """Modular multiplications in square-and-multiply for exponent e >= 1: one squaring per bit after the first,
    one extra multiplication per further 1-bit."""
    return (e.bit_length() - 1) + (bin(e).count("1") - 1)


def fermat_mults(n: int) -> int:
    return power_mults(n - 1)


def miller_rabin_mults(n: int, bases=c06.BASES) -> int:
    """Modular multiplications Miller-Rabin makes when n is a prime larger than every base."""
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    total = 0
    for a in bases:
        total += power_mults(d)
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            total += 1
            x = x * x % n
            if x == n - 1:
                break
    return total


def table(digits: list = DIGITS) -> list:
    """(digits, prime, trial divisions, Fermat multiplications, Miller-Rabin multiplications, sieve cells)."""
    rows = []
    for d in digits:
        p = c06.next_prime(10 ** (d - 1))
        rows.append((d, p, trial_divisions(p), fermat_mults(p), miller_rabin_mults(p), p + 1))
    return rows


def fooled(n: int = 561) -> dict:
    """What each method says about n."""
    return {"trial division": c06.trial(n), "Fermat, base 2": c06.fermat(n, 2), "Miller-Rabin": c06.miller_rabin(n)}


if __name__ == "__main__":
    for row in table():
        print(row)
    print(fooled(561), fooled(41041))
