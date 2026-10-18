import random
import unittest

import ch07_examples as ex
import ch07_solutions as sol


class TestFenwick(unittest.TestCase):
    def test_against_list(self) -> None:
        rng = random.Random(1)
        for _ in range(50):
            vals = [rng.randint(-20, 20) for _ in range(rng.randint(1, 50))]
            t = ex.FenwickTree.from_list(vals)
            t2 = ex.FenwickTree(len(vals))
            for i, v in enumerate(vals):
                t2.add(i, v)
            self.assertEqual(t.box, t2.box)
            for _ in range(100):
                if rng.random() < 0.4:
                    i, d = rng.randrange(len(vals)), rng.randint(-10, 10)
                    vals[i] += d
                    t.add(i, d)
                else:
                    a = rng.randrange(len(vals))
                    b = rng.randrange(a, len(vals))
                    self.assertEqual(t.range_sum(a, b), sum(vals[a:b + 1]))

    def test_lowbit_and_examples(self) -> None:
        self.assertEqual([ex.lowbit(i) for i in (1, 2, 6, 12, 16)], [1, 2, 2, 4, 16])
        rng = random.Random(2)
        for _ in range(100):
            v = [rng.randint(0, 9) for _ in range(rng.randint(0, 15))]
            self.assertEqual(ex.count_smaller_after(v), [sum(1 for y in v[i + 1:] if y < x) for i, x in enumerate(v)])
            self.assertEqual(ex.leaderboard_rank(v, 9), [sum(1 for y in v[:i] if y > x) for i, x in enumerate(v)])


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        rng = random.Random(3)
        for _ in range(100):
            v = [rng.randint(0, 20) for _ in range(rng.randint(0, 20))]
            self.assertEqual(sol.count_inversions(v), sum(1 for i in range(len(v)) for j in range(i + 1, len(v)) if v[i] > v[j]))
            n = rng.randint(1, 15)
            r, model = sol.RangeAddPointQuery(n), [0] * n
            for _ in range(10):
                a = rng.randrange(n)
                b = rng.randrange(a, n)
                d = rng.randint(-3, 3)
                r.add_range(a, b, d)
                for i in range(a, b + 1):
                    model[i] += d
            self.assertEqual([r.value(i) for i in range(n)], model)
            bits = [rng.randint(0, 1) for _ in range(rng.randint(1, 20))]
            t = ex.FenwickTree.from_list(bits)
            ones = [i for i, b in enumerate(bits) if b]
            for k in range(1, len(ones) + 1):
                self.assertEqual(sol.find_kth(t, k), ones[k - 1])


if __name__ == "__main__":
    unittest.main()
