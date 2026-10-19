"""Volume 15, Chapter 10 - Algorithms in Machine Learning: Gradient Descent, Clustering.

Run:  python3 ch10_examples.py
"""

from __future__ import annotations

import math
import random

Point = tuple[float, float]


def mse(w: float, b: float, xs: list[float], ys: list[float]) -> float:
    """Mean squared error of the line y = w*x + b."""
    return sum((w * x + b - y) ** 2 for x, y in zip(xs, ys)) / len(xs)


def gradient_descent_line(xs: list[float], ys: list[float], lr: float, steps: int) -> tuple[float, float, list[float]]:
    """Fit y = w*x + b by repeatedly stepping DOWNHILL on the error surface:
    w -= lr * d(error)/dw,  b -= lr * d(error)/db. Returns (w, b, error after each step)."""
    w = b = 0.0
    n = len(xs)
    history = []
    for _ in range(steps):
        grad_w = sum(2 * (w * x + b - y) * x for x, y in zip(xs, ys)) / n
        grad_b = sum(2 * (w * x + b - y) for x, y in zip(xs, ys)) / n
        w, b = w - lr * grad_w, b - lr * grad_b
        history.append(mse(w, b, xs, ys))
    return w, b, history


def least_squares(xs: list[float], ys: list[float]) -> tuple[float, float]:
    """The exact answer for a straight line (closed form) - to check gradient descent."""
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    w = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    return w, my - w * mx


def kmeans(points: list[Point], k: int, rng: random.Random, iterations: int = 100) -> tuple[list[Point], list[int], float]:
    """Lloyd's algorithm: assign each point to its nearest centre, move each centre to the mean of its points,
    repeat until nothing changes. Returns (centres, labels, total squared distance). A local optimum only."""
    centres = rng.sample(points, k)
    labels = [0] * len(points)
    for _ in range(iterations):
        new_labels = [min(range(k), key=lambda c: math.dist(p, centres[c])) for p in points]
        moved = []
        for c in range(k):
            members = [p for p, lab in zip(points, new_labels) if lab == c]
            moved.append((sum(p[0] for p in members) / len(members), sum(p[1] for p in members) / len(members))
                         if members else centres[c])
        if new_labels == labels and moved == centres:
            break
        labels, centres = new_labels, moved
    cost = sum(math.dist(p, centres[lab]) ** 2 for p, lab in zip(points, labels))
    return centres, labels, cost


def best_of_restarts(points: list[Point], k: int, restarts: int, rng: random.Random) -> float:
    """k-means can get stuck; running it from several random starts and keeping the best is standard practice."""
    return min(kmeans(points, k, rng)[2] for _ in range(restarts))


def make_blobs(centres: list[Point], per: int, spread: float, rng: random.Random) -> list[Point]:
    return [(cx + rng.gauss(0, spread), cy + rng.gauss(0, spread)) for cx, cy in centres for _ in range(per)]


def segment_customers(spend_and_visits: list[Point], groups: int, rng: random.Random) -> list[Point]:
    """Industry example: group customers by (monthly spend, visits) to tailor offers - best of 10 random starts."""
    centres, _, _ = min((kmeans(spend_and_visits, groups, rng) for _ in range(10)), key=lambda run: run[2])
    return sorted((round(x), round(y)) for x, y in centres)


if __name__ == "__main__":
    rng = random.Random(1)
    xs = [float(i) for i in range(10)]
    ys = [3 * x + 2 + rng.gauss(0, 1) for x in xs]
    w, b, hist = gradient_descent_line(xs, ys, 0.01, 2000)
    print(f"gradient descent: w={w:.3f} b={b:.3f} | exact: {tuple(round(v, 3) for v in least_squares(xs, ys))}")
    print("error after 1, 10, 100, 2000 steps:", [round(hist[i], 3) for i in (0, 9, 99, 1999)])
    print("learning rate 0.05 (too big):", [round(gradient_descent_line(xs, ys, 0.05, 30)[2][i]) for i in (0, 9, 29)])
    pts = make_blobs([(0, 0), (10, 0), (5, 8)], 50, 1.0, rng)
    centres, labels, cost = kmeans(pts, 3, rng)
    print("k-means centres:", sorted((round(x, 1), round(y, 1)) for x, y in centres), "cost", round(cost))
    customers = make_blobs([(500, 2), (3000, 8), (12000, 20)], 30, 1.0, rng)
    print("customers, one unlucky run:", sorted((round(x), round(y)) for x, y in kmeans(customers, 3, random.Random(3))[0]))
    print("one run cost vs best of 10:", round(kmeans(customers, 3, random.Random(3))[2]), round(best_of_restarts(customers, 3, 10, rng)))
    print("customer groups:", segment_customers(customers, 3, rng))
