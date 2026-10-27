"""Chapter 30, Section 30.10: every stream summary of Chapters 29 and 30 on the same 20,000 searches.
Memory is counted in stored numbers (counters, registers, or kept hash values)."""
import os
import random
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "chapter_29_counting_stream"))
import ch29_examples as c29   # noqa: E402
import ch30_examples as c30   # noqa: E402


def searches(seed: int = 27) -> list:
    """The stream of Section 30.4: 20,000 searches over 2,000 words, about 5% of them for "dragons"."""
    r = random.Random(seed)
    words = [f"word{i}" for i in range(2000)]
    return [("dragons" if r.random() < 0.05 else r.choice(words)) for _ in range(20000)]


def heavy_hitters(stream: list, k: int = 50, width: int = 1000, depth: int = 4) -> list:
    """(method, numbers stored, estimate for "dragons", true count)."""
    true = Counter(stream)
    mg = c29.misra_gries(stream, k)
    ss = c29.space_saving(stream, k)
    cm = c30.CountMin(width, depth)
    for s in stream:
        cm.add(s)
    return [("exact dictionary", len(true), true["dragons"], true["dragons"]),
            ("Misra-Gries", k - 1, mg.get("dragons", 0), true["dragons"]),
            ("Space-Saving", k, ss.get("dragons", 0), true["dragons"]),
            ("Count-Min", width * depth, cm.estimate("dragons"), true["dragons"])]


def distinct(stream: list) -> list:
    """(method, numbers stored, estimate of the number of different words, true number)."""
    n = len(set(stream))
    return [("exact set", n, n, n),
            ("smallest 64 hashes", 64, round(c29.distinct_estimate(stream, 64)), n),
            ("Flajolet-Martin, 64 copies", 64, round(c29.flajolet_martin(stream, 64)), n),
            ("HyperLogLog, 1,024 registers", 1024, round(c29.hyperloglog(stream, 10)), n)]


if __name__ == "__main__":
    s = searches()
    for row in heavy_hitters(s):
        print(row)
    for row in distinct(s):
        print(row)
