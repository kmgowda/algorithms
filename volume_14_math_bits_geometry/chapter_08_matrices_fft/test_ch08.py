import itertools
import random
import unittest

import ch08_examples as ex
import ch08_solutions as sol


class TestMatricesFFT(unittest.TestCase):
    def test_random(self) -> None:
        rng = random.Random(1)
        a, b = 0, 1
        for n in range(60):
            self.assertEqual(ex.fibonacci_matrix(n), a)
            self.assertEqual(ex.fibonacci_matrix(n, 1000), a % 1000)
            a, b = b, a + b
        t = [0, 1, 1]
        for n in range(30):
            if n >= 3:
                t.append(t[-1] + t[-2] + t[-3])
            self.assertEqual(sol.tribonacci_matrix(n), t[n])
        for _ in range(100):
            p = [rng.randint(-9, 9) for _ in range(rng.randint(1, 40))]
            q = [rng.randint(-9, 9) for _ in range(rng.randint(1, 40))]
            self.assertEqual(ex.poly_mul_fft(p, q), ex.poly_mul_naive(p, q))
            x, y = rng.randint(0, 10 ** 30), rng.randint(0, 10 ** 30)
            self.assertEqual(ex.big_multiply(x, y), x * y)
            m1 = [[rng.randint(0, 5) for _ in range(3)] for _ in range(3)]
            e = rng.randint(0, 6)
            brute = [[int(i == j) for j in range(3)] for i in range(3)]
            for _ in range(e):
                brute = ex.mat_mul(brute, m1)
            self.assertEqual(ex.mat_pow(m1, e), brute)
        adj = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
        for k in range(6):
            walks = sum(1 for w in itertools.product(range(3), repeat=k - 1) if k >= 1
                        and all(adj[u][v] for u, v in zip((0,) + w, w + (0,)))) if k else 1
            self.assertEqual(sol.count_walks(adj, 0, 0, k), walks)
        ways = sol.dice_sum_ways(3)
        for total in range(3, 19):
            self.assertEqual(ways[total], sum(1 for r in itertools.product(range(1, 7), repeat=3) if sum(r) == total))

    def test_examples(self) -> None:
        self.assertEqual(ex.mat_mul([[1, 2], [3, 4]], [[5, 6], [7, 8]]), [[19, 22], [43, 50]])
        self.assertEqual(ex.fibonacci_matrix(10 ** 18, 1_000_000_007), 209783453)
        r = ex.race(2048)
        self.assertLess(r["FFT"], r["naive"])


if __name__ == "__main__":
    unittest.main()
