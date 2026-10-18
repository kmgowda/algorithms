import random
import unittest

import ch06_examples as ex
import ch06_solutions as sol


class TestSegmentTrees(unittest.TestCase):
    def test_against_list(self) -> None:
        rng = random.Random(1)
        for combine, ident, ref in ((lambda a, b: a + b, 0, sum), (min, float("inf"), min), (max, float("-inf"), max)):
            for _ in range(30):
                vals = [rng.randint(-50, 50) for _ in range(rng.randint(1, 40))]
                st = ex.SegmentTree(vals, combine, ident)
                for _ in range(100):
                    if rng.random() < 0.4:
                        i, v = rng.randrange(len(vals)), rng.randint(-50, 50)
                        vals[i] = v
                        st.update(i, v)
                    else:
                        a = rng.randrange(len(vals))
                        b = rng.randrange(a, len(vals))
                        self.assertEqual(st.query(a, b), ref(vals[a:b + 1]))

    def test_lazy_against_list(self) -> None:
        rng = random.Random(2)
        for _ in range(30):
            vals = [rng.randint(0, 20) for _ in range(rng.randint(1, 40))]
            t = ex.LazySumTree(vals)
            for _ in range(100):
                a = rng.randrange(len(vals))
                b = rng.randrange(a, len(vals))
                if rng.random() < 0.5:
                    d = rng.randint(-5, 5)
                    t.add(a, b, d)
                    for i in range(a, b + 1):
                        vals[i] += d
                else:
                    self.assertEqual(t.total(a, b), sum(vals[a:b + 1]))

    def test_flights(self) -> None:
        self.assertEqual(ex.cheapest_flight_in_window([320, 280, 300, 410, 260, 290], [(4, 500), (2, 250)], (1, 4)), 250)


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        na = sol.NumArray([1, 3, 5])
        self.assertEqual(na.sum_range(0, 2), 9)
        na.update(1, 2)
        self.assertEqual(na.sum_range(0, 2), 8)
        self.assertEqual(sol.max_temperatures([21, 25, 19, 30, 22], [(0, 2), (1, 4)]), [25, 30])
        self.assertEqual(sol.corporate_bookings([(1, 2, 10), (2, 3, 20), (2, 5, 25)], 5), [10, 55, 45, 25, 25])
        self.assertEqual(sol.gcd_ranges([12, 18, 24, 7], [(0, 2), (0, 3)]), [6, 1])


if __name__ == "__main__":
    unittest.main()
