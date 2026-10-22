"""Volume 6, Chapter 20 - Estimating with Random Trials: Monte Carlo estimates and how accurate they are.

Run:  python3 ch20_examples.py
"""

from __future__ import annotations

import math
import random


def estimate_pi(trials: int, rng) -> float:
    """Darts at a unit square: the fraction inside the quarter circle is pi/4 (Figure 20.1)."""
    if trials <= 0:
        raise ValueError("at least one trial is needed")
    inside = sum(1 for _ in range(trials) if rng.random() ** 2 + rng.random() ** 2 <= 1)
    return 4 * inside / trials


def shared_birthday(people: int, trials: int, rng) -> float:
    """Fraction of trial groups in which two people share a birthday (365 days)."""
    hits = 0
    for _ in range(trials):
        days = [rng.randrange(365) for _ in range(people)]
        hits += len(set(days)) < people
    return hits / trials


def shared_birthday_exact(people: int) -> float:
    p = 1.0
    for i in range(people):
        p *= (365 - i) / 365
    return 1 - p


def queue_wait(trials: int, rng) -> float:
    """Average wait at a desk: a visitor arrives each minute with chance 0.5; serving takes 1 or 2 minutes equally often.
    The answer has no simple formula, so we estimate it."""
    total_wait, served = 0, 0
    for _ in range(trials):
        free_at, wait = 0, 0
        for minute in range(60):
            if rng.random() < 0.5:
                start = max(minute, free_at)
                wait += start - minute
                free_at = start + rng.choice((1, 2))
                served += 1
        total_wait += wait
    return total_wait / served


def standard_error(p: float, trials: int) -> float:
    """Standard error of a fraction estimated from `trials` independent yes/no trials: sqrt(p (1 - p) / N)."""
    return math.sqrt(p * (1 - p) / trials)


def pi_interval(trials: int, rng) -> tuple[float, float, float]:
    """Estimate pi with a 95% confidence interval: estimate plus or minus 2 standard errors (of 4 x the fraction)."""
    inside = sum(1 for _ in range(trials) if rng.random() ** 2 + rng.random() ** 2 <= 1)
    f = inside / trials
    se = 4 * math.sqrt(f * (1 - f) / trials)
    return 4 * f, 4 * f - 2 * se, 4 * f + 2 * se


def coverage(trials: int, repeats: int, seed: int) -> float:
    """How often the 95% interval really contains pi, over many independent estimates."""
    rng = random.Random(seed)
    hits = 0
    for _ in range(repeats):
        _, lo, hi = pi_interval(trials, rng)
        hits += lo <= math.pi <= hi
    return hits / repeats


def trials_needed(p: float, half_width: float, scale: float = 1.0) -> int:
    """Trials so that 2 standard errors of scale x fraction are at most half_width."""
    return math.ceil((2 * scale) ** 2 * p * (1 - p) / half_width ** 2)


def mc_integral(f, a: float, b: float, trials: int, rng) -> tuple[float, float]:
    """Monte Carlo integration: (b - a) x the average of f at random points, with its standard error."""
    vals = [f(a + (b - a) * rng.random()) for _ in range(trials)]
    mean = sum(vals) / trials
    var = sum((v - mean) ** 2 for v in vals) / (trials - 1)
    return (b - a) * mean, (b - a) * math.sqrt(var / trials)


def mc_integral_antithetic(f, a: float, b: float, pairs: int, rng) -> tuple[float, float]:
    """The same with mirrored pairs u and 1 - u, whose errors partly cancel (variance reduction)."""
    vals = []
    for _ in range(pairs):
        u = rng.random()
        vals.append((f(a + (b - a) * u) + f(a + (b - a) * (1 - u))) / 2)
    mean = sum(vals) / pairs
    var = sum((v - mean) ** 2 for v in vals) / (pairs - 1)
    return (b - a) * mean, (b - a) * math.sqrt(var / pairs)


def event_on_time(trials: int, rng) -> float:
    """Four talks of 15 to 25 minutes (uniform) plus a 10-minute break: chance of finishing within 95 minutes."""
    ok = sum(1 for _ in range(trials) if sum(rng.uniform(15, 25) for _ in range(4)) + 10 <= 95)
    return ok / trials


def event_on_time_exact() -> float:
    """Irwin-Hall: the sum of 4 uniforms on 0..1 is at most 2.5 with chance (1/4!) sum (-1)^k C(4, k) (2.5 - k)^4."""
    return sum((-1) ** k * math.comb(4, k) * (2.5 - k) ** 4 for k in range(3)) / math.factorial(4)


if __name__ == "__main__":
    rng = random.Random(20)
    for n in (100, 10_000, 1_000_000):
        e = estimate_pi(n, rng)
        print(n, e, round(abs(e - math.pi), 4))
    print(shared_birthday(23, 20000, rng), round(shared_birthday_exact(23), 4), round(shared_birthday_exact(50), 4))
    print(round(queue_wait(5000, rng), 3))
    p = math.pi / 4
    print([round(4 * standard_error(p, n), 4) for n in (100, 10_000, 1_000_000)])
    print([round(x, 4) for x in pi_interval(10_000, random.Random(1))], coverage(1000, 2000, 2))
    print(trials_needed(p, 0.001, scale=4), trials_needed(0.5, 0.01))
    f = lambda x: math.exp(-x * x)
    exact = math.sqrt(math.pi) / 2 * math.erf(1)
    print(round(exact, 6), [round(v, 5) for v in mc_integral(f, 0, 1, 10_000, random.Random(3))],
          [round(v, 5) for v in mc_integral_antithetic(f, 0, 1, 5_000, random.Random(3))])
    print(event_on_time(100_000, random.Random(4)), round(event_on_time_exact(), 4))
