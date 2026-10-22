"""Volume 4, Chapter 14 - Thinking Problems (Section 14.14): model solutions that can be run.

1. expected_sum_of_squares: E[sum n_i^2] = n + (n^2 - n) * sum p_i^2 for any bucket probabilities p_i.
2. sort_by_distance: sort n points of the unit disc by distance from the centre in expected O(n) time.
3. leo_prediction against exact_average_sum_of_squares: the flaw E[X^2] = E[X]^2.

Run:  python3 ch14_solutions.py
"""

from __future__ import annotations

import itertools


def expected_sum_of_squares(p: list[float], n: int) -> float:
    """Expected sum of squared bucket sizes when n keys fall independently, key into bucket i with chance p[i]."""
    return n + (n * n - n) * sum(q * q for q in p)


def linear_density_buckets(n: int) -> list[float]:
    """Bucket chances for keys with density 2x on [0, 1) (bounded by c = 2), with n equal buckets."""
    return [((i + 1) ** 2 - i ** 2) / n ** 2 for i in range(n)]


def power_eight_buckets(n: int) -> list[float]:
    """Bucket chances for the bunched keys u ** 8 of Section 14.5 (unbounded density near 0)."""
    return [((i + 1) / n) ** 0.125 - (i / n) ** 0.125 for i in range(n)]


def sort_by_distance(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Sort points of the unit disc by distance from the centre: bucket by the squared distance, which is spread
    evenly over [0, 1) when the points are spread evenly over the disc, then insertion-sort each bucket."""
    n = len(points)
    buckets = [[] for _ in range(n)]
    for p in points:
        d = p[0] * p[0] + p[1] * p[1]
        buckets[min(int(d * n), n - 1)].append((d, p))
    out = []
    for b in buckets:
        for i in range(1, len(b)):                      # insertion sort on the squared distance: stable
            item, j = b[i], i - 1
            while j >= 0 and b[j][0] > item[0]:
                b[j + 1] = b[j]
                j -= 1
            b[j + 1] = item
        out += [p for _, p in b]
    return out


def leo_prediction(n: int, m: int) -> float:
    """Leo's flawed estimate of the sum of squared bucket sizes: m * (average size) ** 2 = n * n / m."""
    return n * n / m


def exact_average_sum_of_squares(n: int, m: int) -> float:
    """The true average over all m ** n equally likely scatterings of n keys into m buckets (small n, m only)."""
    total = 0
    for choice in itertools.product(range(m), repeat=n):
        sizes = [0] * m
        for b in choice:
            sizes[b] += 1
        total += sum(s * s for s in sizes)
    return total / m ** n


if __name__ == "__main__":
    n = 10_000
    print(expected_sum_of_squares(linear_density_buckets(n), n), expected_sum_of_squares([1 / n] * n, n))
    print(expected_sum_of_squares(power_eight_buckets(n), n), n * power_eight_buckets(n)[0])
    print(sort_by_distance([(0.5, 0.5), (0.1, 0.0), (0.0, -0.9)]))
    print(leo_prediction(2, 2), exact_average_sum_of_squares(2, 2))
