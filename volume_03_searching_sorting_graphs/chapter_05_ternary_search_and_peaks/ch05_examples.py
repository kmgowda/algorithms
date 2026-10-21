"""Volume 3, Chapter 5 - Ternary Search and Peaks.

Run:  python3 ch05_examples.py
"""

from __future__ import annotations

VISITORS = [12, 20, 31, 45, 58, 66, 61, 50, 38, 25, 16, 9]     # visitors per hour from 9:00; rises, then falls
BUMPY = [3, 8, 6, 9, 14, 11, 7, 10, 5]                         # several local peaks


def peak_by_slope(a: list, trace: list | None = None) -> int:
    """Binary search on the slope: if a[mid] < a[mid+1] a peak lies to the right (Figure 5.2)."""
    lo, hi = 0, len(a) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        rising = a[mid] < a[mid + 1]
        if trace is not None:
            trace.append((lo, hi, mid, a[mid], a[mid + 1], rising))
        if rising:
            lo = mid + 1
        else:
            hi = mid
    return lo


def ternary_max(f, lo: int, hi: int, trace: list | None = None) -> int:
    """Largest value of a unimodal f on whole numbers lo..hi by ternary search (Figure 5.4)."""
    while hi - lo > 2:
        m1 = lo + (hi - lo) // 3
        m2 = hi - (hi - lo) // 3
        if trace is not None:
            trace.append((lo, hi, m1, f(m1), m2, f(m2)))
        if f(m1) < f(m2):
            lo = m1 + 1
        else:
            hi = m2 - 1 if f(m1) > f(m2) else m2
    return max(range(lo, hi + 1), key=f)


def comfort(height_cm: int) -> int:
    """Reading-lamp comfort score: best at 46 cm above the desk, worse either way."""
    return 1000 - (height_cm - 46) ** 2


def is_peak(a: list, i: int) -> bool:
    return (i == 0 or a[i - 1] <= a[i]) and (i == len(a) - 1 or a[i + 1] <= a[i])


def is_unimodal(a: list) -> bool:
    """Section 5.8: strictly rises then strictly falls (either part may be empty)."""
    i = 0
    while i + 1 < len(a) and a[i] < a[i + 1]:
        i += 1
    while i + 1 < len(a) and a[i] > a[i + 1]:
        i += 1
    return i == len(a) - 1


if __name__ == "__main__":
    t = []
    print(peak_by_slope(VISITORS, t), t)
    t = []
    print(peak_by_slope(BUMPY, t), t, [i for i in range(len(BUMPY)) if is_peak(BUMPY, i)])
    t = []
    print(ternary_max(comfort, 0, 100, t), len(t), t[:4])
