"""Chapter 24, Section 24.9: the strategies behind the searches. Each function returns the positions a strategy
looks at, in order, on a sorted shelf; the number of looks is the length of that list."""

SHELF16 = list(range(10, 170, 10))        # sixteen call numbers 10, 20, ..., 160


def brute_force(a: list, key) -> list:
    """Look at every book from the left until the key is found."""
    out = []
    for i, v in enumerate(a):
        out.append(i)
        if v == key:
            break
    return out


def halves_both(a: list, key) -> list:
    """Divide and conquer that keeps both halves: search the left half, then the right half."""
    out = []

    def go(lo, hi):
        if hi - lo <= 0:
            return False
        if hi - lo == 1:
            out.append(lo)
            return a[lo] == key
        mid = (lo + hi) // 2
        return go(lo, mid) or go(mid, hi)
    go(0, len(a))
    return out


def halves_one(a: list, key, lo: int = 0, hi: int | None = None) -> list:
    """Decrease and conquer: look at the middle and keep only the half that can hold the key (binary search)."""
    hi = len(a) - 1 if hi is None else hi
    out = []
    while lo <= hi:
        mid = (lo + hi) // 2
        out.append(mid)
        if a[mid] == key:
            break
        lo, hi = (mid + 1, hi) if a[mid] < key else (lo, mid - 1)
    return out


def doubling(a: list, key) -> list:
    """Look at positions 0, 1, 3, 7, 15, ... until one is at least the key, then binary-search the last stretch."""
    if not a:
        return []
    out, i, prev = [], 0, -1
    while True:
        i = min(i, len(a) - 1)
        out.append(i)
        if a[i] >= key or i == len(a) - 1:
            break
        prev, i = i, 2 * i + 1
    if a[i] == key:
        return out
    return out + halves_one(a, key, prev + 1, i - 1)


STRATEGIES = {"brute force": brute_force, "halves, both kept": halves_both, "halves, one kept": halves_one,
              "doubling, then halving": doubling}


def compare(key, a: list = SHELF16) -> dict:
    return {name: f(a, key) for name, f in STRATEGIES.items()}


if __name__ == "__main__":
    for key in (30, 150):
        for name, pos in compare(key).items():
            print(key, name, len(pos), pos)
    big = list(range(1_000_000))
    for key in (5, 999_999):
        print(key, {n: len(f(big, key)) for n, f in STRATEGIES.items() if n != "halves, both kept"})
