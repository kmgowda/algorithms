import math
import random
import unittest
from collections import Counter

import ch10_examples as ex
import ch10_solutions as sol


def josephus_sim(n, k):
    people, i = list(range(n)), 0
    while len(people) > 1:
        i = (i + k - 1) % len(people)
        people.pop(i)
    return people[0]


class TestDecreaseTransform(unittest.TestCase):
    def test_random(self) -> None:
        rng = random.Random(1)
        for _ in range(200):
            v = [rng.randint(0, 9) for _ in range(rng.randint(1, 20))]
            self.assertEqual(ex.insertion_sort(v), sorted(v))
            self.assertEqual(ex.heap_sort(v), sorted(v))
            self.assertEqual(ex.has_duplicate_presort(v), len(set(v)) < len(v))
            m = ex.mode_presort(v)
            self.assertEqual(Counter(v)[m], max(Counter(v).values()))
            a, b = rng.randint(1, 500), rng.randint(1, 500)
            self.assertEqual(ex.gcd(a, b), math.gcd(a, b))
            self.assertEqual(ex.lcm(a, b), a * b // math.gcd(a, b))
            g, x, y = sol.extended_gcd(a, b)
            self.assertEqual((g, a * x + b * y), (math.gcd(a, b), g))
            n, k = rng.randint(1, 15), rng.randint(1, 5)
            self.assertEqual(ex.josephus(n, k), josephus_sim(n, k))
            coeffs = [rng.randint(-5, 5) for _ in range(rng.randint(1, 6))]
            xv = rng.randint(-4, 4)
            self.assertEqual(ex.horner(coeffs, xv), sum(c * xv ** i for i, c in enumerate(coeffs)))
            num = rng.randint(0, 10 ** 6)
            self.assertEqual(sol.integer_sqrt(num), math.isqrt(num))
            t = rng.randint(0, 20)
            self.assertEqual(sol.two_sum_presort(v, t), any(v[i] + v[j] == t for i in range(len(v)) for j in range(i + 1, len(v))))

    def test_fake_coin(self) -> None:
        for n in range(1, 82):
            for fake in range(n):
                coins = [10] * n
                coins[fake] = 9
                idx, w = ex.find_fake_coin(coins)
                self.assertEqual(idx, fake)
                self.assertLessEqual(w, max(1, math.ceil(math.log(n, 3) - 1e-9)))

    def test_examples(self) -> None:
        self.assertEqual(ex.bus_timetable_meeting([12, 18, 30]), 180)
        self.assertEqual(ex.josephus(7, 3), 3)
        self.assertEqual(len(sol.subsets_decrease(["a", "b", "c"])), 8)


if __name__ == "__main__":
    unittest.main()
