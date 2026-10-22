import random
import unittest

import ch18_examples as ex
import ch18_solutions as sol


class TestChapter18Solutions(unittest.TestCase):
    def test_stretches_nest_or_are_disjoint(self) -> None:
        for n in (1, 2, 8, 37):
            for i in range(1, n + 1):
                for j in range(i + 1, n + 1):
                    a, b = set(sol.stretch(i)), set(sol.stretch(j))
                    self.assertTrue(not a & b or a <= b)
                for day in range(1, n + 1):          # Add(day) visits exactly the boxes covering day
                    f = ex.Fenwick([0] * n)
                    self.assertEqual(f.add(day, 1), [i for i in range(1, n + 1) if day in sol.stretch(i)])

    def test_first_reaching(self) -> None:
        self.assertIsNone(sol.first_reaching(ex.Fenwick([]), 1))
        one = ex.Fenwick([7])
        self.assertEqual((sol.first_reaching(one, 1), sol.first_reaching(one, 7), sol.first_reaching(one, 8)),
                         (1, 1, None))
        with self.assertRaises(ValueError):
            sol.first_reaching(one, 0)
        f = ex.Fenwick(ex.DAYS)
        self.assertEqual([sol.first_reaching(f, s) for s in (1, 4, 5, 15, 31, 32)], [1, 2, 3, 6, 8, None])
        self.assertEqual(sol.first_reaching(ex.Fenwick([0, 0, 5]), 1), 3)
        self.assertEqual(sol.kth_lowest_score([72, 95, 41, 88, 60], 2), 60)
        rng = random.Random(8)
        for _ in range(300):
            v = [rng.randint(0, 5) for _ in range(rng.randint(1, 40))]
            f, s = ex.Fenwick(v), rng.randint(1, sum(v) + 2)
            run, want = 0, None
            for i, x in enumerate(v, 1):
                run += x
                if run >= s:
                    want = i
                    break
            self.assertEqual(sol.first_reaching(f, s), want)

    def test_right_to_left_build_is_wrong(self) -> None:
        self.assertEqual(sol.build_right_to_left([]), [])
        self.assertEqual(sol.build_right_to_left([7]), [7])
        self.assertEqual(sol.build_right_to_left([3, 1]), [3, 4])
        self.assertEqual(sol.build_right_to_left(ex.DAYS), [3, 4, 4, 6, 5, 14, 2, 18])
        self.assertNotEqual(sol.build_right_to_left(ex.DAYS), ex.Fenwick(ex.DAYS).tree[1:])


if __name__ == "__main__":
    unittest.main()
