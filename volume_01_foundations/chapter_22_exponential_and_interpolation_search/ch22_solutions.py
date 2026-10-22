"""Volume 1, Chapter 22, Thinking Problem 2 - measuring the reel without winding to its end.

Gallop 1, 2, 4, 8, ... until a read falls off the end, then halve the last gap, keeping the invariant
"entry lo exists, entry hi does not". The length n is found in about 2 log2 n reads.

Run:  python3 ch22_solutions.py
"""

from __future__ import annotations

from ch22_examples import Reel


def reel_length(reel: Reel) -> int:
    """Number of entries on a reel whose read(i) returns None past the end."""
    if reel.read(0) is None:
        return 0
    hi = 1
    while reel.read(hi) is not None:
        hi *= 2                                   # gallop: entry hi // 2 exists
    lo = hi // 2                                  # entry lo exists, entry hi does not
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if reel.read(mid) is not None:
            lo = mid
        else:
            hi = mid
    return hi


if __name__ == "__main__":
    r = Reel(range(3, 3000, 3))                   # 999 entries
    print(reel_length(r), r.reads)
