"""Volume 2, Chapter 12 - Profiling Real Code: Timing, Profilers, Percentiles, and Fake Speedups.

Run:  python3 ch12_examples.py
"""

from __future__ import annotations

import cProfile
import io
import math
import pstats
import random
import timeit
from typing import Callable


# ------------------------------------------------------------------ a slow report job with a hidden hotspot
def load_orders(n: int, seed: int = 0) -> list[tuple[int, str, float]]:
    """Fake shop orders: (order_id, customer, amount)."""
    rng = random.Random(seed)
    customers = [f"cust{i}" for i in range(n // 10 + 1)]
    return [(i, rng.choice(customers), round(rng.uniform(5, 500), 2)) for i in range(n)]


def vip_customers_slow(orders: list[tuple[int, str, float]], vip_list: list[str]) -> float:
    """Total spent by VIP customers. Hotspot: `in vip_list` is a hidden O(len(vip_list)) loop."""
    total = 0.0
    for _, customer, amount in orders:
        if customer in vip_list:
            total += amount
    return round(total, 2)


def vip_customers_fast(orders: list[tuple[int, str, float]], vip_list: list[str]) -> float:
    """Same answer: convert the VIP list to a set ONCE, so each check is O(1) on average."""
    vips = set(vip_list)
    total = 0.0
    for _, customer, amount in orders:
        if customer in vips:
            total += amount
    return round(total, 2)


def report_text_slow(orders: list[tuple[int, str, float]]) -> str:
    """Builds a long string with += (may copy the growing string again and again)."""
    text = ""
    for order_id, customer, amount in orders:
        text += f"{order_id},{customer},{amount}\n"
    return text


def report_text_fast(orders: list[tuple[int, str, float]]) -> str:
    """Collect pieces in a list, join once (V1-C8)."""
    return "".join(f"{order_id},{customer},{amount}\n" for order_id, customer, amount in orders)


def nightly_job(orders: list[tuple[int, str, float]], vip_list: list[str], fast: bool) -> tuple[float, int]:
    """The whole job: VIP total + CSV report. Returns (vip total, report length)."""
    if fast:
        return vip_customers_fast(orders, vip_list), len(report_text_fast(orders))
    return vip_customers_slow(orders, vip_list), len(report_text_slow(orders))


# ------------------------------------------------------------------ profiling
def profile_top_functions(function: Callable[[], object], top: int = 5) -> list[tuple[str, float]]:
    """Run `function` under cProfile and return the `top` functions by their OWN time (excluding callees)."""
    profiler = cProfile.Profile()
    profiler.enable()
    function()
    profiler.disable()
    stats = pstats.Stats(profiler, stream=io.StringIO())
    rows = []
    for (filename, line, name), (_, _, own_time, _, _) in stats.stats.items():  # type: ignore[attr-defined]
        rows.append((name, own_time))
    rows.sort(key=lambda row: row[1], reverse=True)
    return rows[:top]


def compare_speed(slow: Callable[[], object], fast: Callable[[], object], number: int = 3) -> float:
    """How many times faster is `fast` than `slow`? (best of 3 batches each, using timeit)."""
    slow_time = min(timeit.repeat(slow, number=number, repeat=3))
    fast_time = min(timeit.repeat(fast, number=number, repeat=3))
    return slow_time / fast_time


# ------------------------------------------------------------------ percentiles
def percentile(values: list[float], p: float) -> float:
    """Nearest-rank percentile: the smallest value with at least p% of the values at or below it."""
    if not values:
        raise ValueError("no values")
    if not 0 < p <= 100:
        raise ValueError("p must be in (0, 100]")
    ordered = sorted(values)
    rank = math.ceil(p / 100 * len(ordered))
    return ordered[rank - 1]


def latency_summary(latencies_ms: list[float]) -> dict[str, float]:
    """Industry example: how web teams summarize response times."""
    return {
        "mean": round(sum(latencies_ms) / len(latencies_ms), 1),
        "p50": percentile(latencies_ms, 50),
        "p95": percentile(latencies_ms, 95),
        "p99": percentile(latencies_ms, 99),
        "max": max(latencies_ms),
    }


def simulated_latencies(requests: int, seed: int = 1) -> list[float]:
    """Most requests are fast; a few hit a slow database path."""
    rng = random.Random(seed)
    result = []
    for _ in range(requests):
        if rng.random() < 0.03:
            result.append(round(rng.uniform(300, 900), 1))      # slow path
        else:
            result.append(round(rng.uniform(20, 60), 1))        # fast path
    return result


# ------------------------------------------------------------------ Amdahl's law
def amdahl_speedup(fraction_improved: float, factor: float) -> float:
    """Overall speedup when `fraction_improved` of the run time becomes `factor` times faster."""
    if not 0 <= fraction_improved <= 1 or factor <= 0:
        raise ValueError("fraction in [0, 1], factor > 0")
    return 1 / ((1 - fraction_improved) + fraction_improved / factor)


if __name__ == "__main__":
    orders = load_orders(20_000)
    vips = [f"cust{i}" for i in range(0, 2000, 3)]
    assert nightly_job(orders, vips, fast=False) == nightly_job(orders, vips, fast=True)
    print("Top functions (slow job):", [(name, round(t, 3)) for name, t in
                                        profile_top_functions(lambda: nightly_job(orders, vips, False), 3)])
    print("VIP check speed-up:", round(compare_speed(lambda: vip_customers_slow(orders, vips),
                                                     lambda: vip_customers_fast(orders, vips)), 1), "x")
    print("Report text speed-up:", round(compare_speed(lambda: report_text_slow(orders),
                                                       lambda: report_text_fast(orders)), 2), "x")
    print("Latency summary:", latency_summary(simulated_latencies(10_000)))
    print("Amdahl - speed up 10% of the job 100x:", round(amdahl_speedup(0.1, 100), 3),
          "| speed up 90% of it 2x:", round(amdahl_speedup(0.9, 2), 3))
