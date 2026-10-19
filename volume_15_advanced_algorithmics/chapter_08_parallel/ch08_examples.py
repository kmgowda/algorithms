"""Volume 15, Chapter 8 - Parallel and Concurrent Algorithms: Fork-Join, Parallel Merge Sort.

Python threads share one interpreter lock for pure-Python code, so CPU-bound work uses PROCESSES here.

Run:  python3 ch08_examples.py
"""

from __future__ import annotations

import heapq
import random
import time
from concurrent.futures import ProcessPoolExecutor


def count_primes_in(bounds: tuple[int, int]) -> int:
    """CPU-heavy work for one chunk: count primes in [lo, hi) by trial division."""
    lo, hi = bounds
    count = 0
    for n in range(max(lo, 2), hi):
        d = 2
        while d * d <= n:
            if n % d == 0:
                break
            d += 1
        else:
            count += 1
    return count


def parallel_count_primes(limit: int, workers: int) -> int:
    """FORK: split the range into chunks, one task each; JOIN: add the partial counts."""
    step = -(-limit // (workers * 4))                       # a few chunks per worker balances the load
    chunks = [(lo, min(lo + step, limit)) for lo in range(0, limit, step)]
    if workers == 1:
        return sum(map(count_primes_in, chunks))
    with ProcessPoolExecutor(workers) as pool:
        return sum(pool.map(count_primes_in, chunks))


def parallel_merge_sort(values: list[int], workers: int) -> list[int]:
    """Sort one slice per worker in parallel, then k-way merge the sorted slices (V7-C3)."""
    if workers == 1 or len(values) < 2:
        return sorted(values)
    size = -(-len(values) // workers)
    slices = [values[i:i + size] for i in range(0, len(values), size)]
    with ProcessPoolExecutor(workers) as pool:
        sorted_slices = list(pool.map(sorted, slices))
    return list(heapq.merge(*sorted_slices))


def prefix_sums_rounds(values: list[int]) -> tuple[list[int], int, int]:
    """Parallel prefix sums (Hillis-Steele): in round r every position adds the value 2^r places to its left.
    All additions in a round are independent, so with enough processors each round takes one step.
    Returns (prefix sums, rounds = SPAN, total additions = WORK)."""
    out, step, rounds, work = list(values), 1, 0, 0
    while step < len(out):
        out = [out[i] + out[i - step] if i >= step else out[i] for i in range(len(out))]
        work += len(out) - step
        step *= 2
        rounds += 1
    return out, rounds, work


def amdahl_speedup(parallel_fraction: float, processors: int) -> float:
    """Amdahl's law (V2-C12): the serial part limits the speed-up, however many processors you add."""
    return 1 / ((1 - parallel_fraction) + parallel_fraction / processors)


def timed(fn, *args) -> tuple[object, float]:
    start = time.perf_counter()
    result = fn(*args)
    return result, time.perf_counter() - start


def render_tiles(tiles: int, workers: int) -> int:
    """Industry example: an image split into tiles rendered independently (here: prime counting stands in
    for the per-tile work) - 'embarrassingly parallel' work scales almost perfectly."""
    return parallel_count_primes(tiles * 2000, workers)


if __name__ == "__main__":
    for w in (1, 2, 4, 8):
        count, secs = timed(parallel_count_primes, 400000, w)
        print(f"primes below 400000 with {w} worker(s): {count} in {secs:.2f} s")
    rng = random.Random(1)
    data = [rng.randint(0, 10 ** 9) for _ in range(10 ** 6)]
    for w in (1, 4):
        result, secs = timed(parallel_merge_sort, data, w)
        print(f"sort 10^6 numbers with {w} worker(s): {secs:.2f} s, correct = {result == sorted(data)}")
    print(prefix_sums_rounds([1, 2, 3, 4, 5, 6, 7, 8]))
    print({p: round(amdahl_speedup(0.9, p), 2) for p in (1, 2, 4, 8, 16, 1000)})
