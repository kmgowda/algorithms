import random
import unittest

import ch26_examples as ex
import ch26_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_horner(self) -> None:
        r = random.Random(26)
        for _ in range(200):
            coeffs = [r.randint(-9, 9) for _ in range(r.randint(0, 8))]
            x = r.randint(-5, 5)
            k = len(coeffs) - 1
            self.assertEqual(ex.horner(coeffs, x, [0]), sum(c * x ** (k - i) for i, c in enumerate(coeffs)))

    def test_pair_with_difference(self) -> None:
        self.assertEqual(sol.pair_with_difference([58, 25, 91, 12, 70, 47, 84, 31, 63], 23), (47, 70))
        self.assertIsNone(sol.pair_with_difference([1, 5, 9], 3))
        self.assertEqual(sol.pair_with_difference([4, 4], 0), (4, 4))
        self.assertIsNone(sol.pair_with_difference([4], 0))
        r = random.Random(2)
        for _ in range(300):
            v = [r.randint(0, 30) for _ in range(r.randint(0, 10))]
            d = r.randint(0, 10)
            want = any(v[j] - v[i] == d for i in range(len(v)) for j in range(len(v)) if i != j)
            got = sol.pair_with_difference(v, d)
            self.assertEqual(got is not None, want)
            if got:
                self.assertEqual(got[1] - got[0], d)

    def test_order_mistake(self) -> None:
        self.assertEqual((ex.horner([3, 2, 1], 10, [0]), sol.horner_low_first([1, 2, 3], 10)), (321, 123))


if __name__ == "__main__":
    unittest.main()
