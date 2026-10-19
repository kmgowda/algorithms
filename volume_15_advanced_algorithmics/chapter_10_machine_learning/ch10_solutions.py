"""Volume 15, Chapter 10 - Solutions to the exercises."""

from __future__ import annotations

import math
import random

from ch10_examples import Point, kmeans


def minimise_1d(f, df, x0: float, lr: float, steps: int) -> float:
    """Exercise 1: gradient descent on any smooth one-variable function, given its derivative."""
    x = x0
    for _ in range(steps):
        x -= lr * df(x)
    return x


def elbow(points: list[Point], max_k: int, rng: random.Random) -> list[float]:
    """Exercise 2: cost for k = 1..max_k (best of 5 starts). The 'elbow' where gains flatten suggests k."""
    return [min(kmeans(points, k, rng)[2] for _ in range(5)) for k in range(1, max_k + 1)]


def scale_features(points: list[Point]) -> list[Point]:
    """Exercise 3: put every feature on the same scale (mean 0, standard deviation 1) so one large-valued
    feature (rupees) doesn't drown out a small one (visits)."""
    out = []
    cols = list(zip(*points))
    stats = [(sum(c) / len(c), math.sqrt(sum((v - sum(c) / len(c)) ** 2 for v in c) / len(c)) or 1.0) for c in cols]
    for p in points:
        out.append(tuple((v - m) / s for v, (m, s) in zip(p, stats)))
    return out


if __name__ == "__main__":
    print(round(minimise_1d(lambda x: (x - 3) ** 2, lambda x: 2 * (x - 3), 0.0, 0.1, 100), 4))
    rng = random.Random(0)
    pts = [(rng.gauss(cx, 0.5), rng.gauss(0, 0.5)) for cx in (0, 5, 10) for _ in range(20)]
    print([round(c) for c in elbow(pts, 5, rng)], scale_features([(100, 1), (300, 3)]))
