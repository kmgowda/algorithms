"""Volume 2, Chapter 12 - Solutions to the exercises."""

from __future__ import annotations

from ch12_examples import amdahl_speedup, percentile


def max_overall_speedup(fraction_improved: float) -> float:
    """Exercise 2: even an infinitely fast fix can't beat 1 / (1 - fraction)."""
    if fraction_improved >= 1:
        return float("inf")
    return 1 / (1 - fraction_improved)


def tax_slow(prices: list[float], region: str) -> list[float]:
    """Exercise 3 (before): the rate lookup is repeated inside the loop."""
    result = []
    for price in prices:
        rates = {"north": 0.05, "south": 0.08, "east": 0.12}   # rebuilt every iteration
        result.append(round(price * (1 + rates[region]), 2))
    return result


def tax_fast(prices: list[float], region: str) -> list[float]:
    """Exercise 3 (after): hoist the loop-invariant work out of the loop."""
    rate = {"north": 0.05, "south": 0.08, "east": 0.12}[region]
    return [round(price * (1 + rate), 2) for price in prices]


def meets_slo(latencies_ms: list[float], p: float, limit_ms: float) -> bool:
    """Exercise 4: does the p-th percentile stay within the service-level objective?"""
    return percentile(latencies_ms, p) <= limit_ms


def best_plan(fraction_a: float, factor_a: float, fraction_b: float, factor_b: float) -> str:
    """Exercise 5: which single optimization gives the bigger overall speedup?"""
    a = amdahl_speedup(fraction_a, factor_a)
    b = amdahl_speedup(fraction_b, factor_b)
    return "A" if a > b else "B"


if __name__ == "__main__":
    print(max_overall_speedup(0.8), tax_fast([100, 250], "south") == tax_slow([100, 250], "south"))
    print(meets_slo([10, 20, 30, 400], 75, 50), best_plan(0.6, 2, 0.2, 50))
