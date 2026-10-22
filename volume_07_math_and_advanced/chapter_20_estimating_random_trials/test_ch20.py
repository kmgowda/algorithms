import math
import random
import unittest

import ch20_examples as ex


class TestChapter20(unittest.TestCase):
    def test_examples(self) -> None:
        rng = random.Random(20)
        got = [ex.estimate_pi(n, rng) for n in (100, 10_000, 1_000_000)]
        self.assertEqual(got, [3.32, 3.1316, 3.142832])
        self.assertEqual((ex.shared_birthday(23, 20000, rng), round(ex.shared_birthday_exact(23), 4), round(ex.shared_birthday_exact(50), 4)), (0.50755, 0.5073, 0.9704))
        self.assertEqual(round(ex.queue_wait(5000, rng), 3), 0.862)

    def test_every_case(self) -> None:
        with self.assertRaises(ValueError):
            ex.estimate_pi(0, random.Random(1))
        self.assertEqual((ex.shared_birthday_exact(1), ex.shared_birthday_exact(366)), (0.0, 1.0))
        self.assertEqual(ex.shared_birthday(1, 100, random.Random(1)), 0.0)
        self.assertLess(abs(ex.estimate_pi(200000, random.Random(5)) - math.pi), 0.02)


class TestDepth(unittest.TestCase):
    def test_error_and_confidence(self) -> None:
        import math
        p = math.pi / 4
        self.assertEqual([round(4 * ex.standard_error(p, n), 4) for n in (100, 10_000, 1_000_000)], [0.1642, 0.0164, 0.0016])
        self.assertEqual([round(x, 4) for x in ex.pi_interval(10_000, random.Random(1))], [3.1416, 3.1088, 3.1744])
        self.assertAlmostEqual(ex.coverage(1000, 2000, 2), 0.95, delta=0.02)
        self.assertEqual((ex.trials_needed(p, 0.001, scale=4), ex.trials_needed(0.5, 0.01)), (10787065, 10000))

    def test_integrals_and_event(self) -> None:
        import math
        f = lambda x: math.exp(-x * x)
        exact = math.sqrt(math.pi) / 2 * math.erf(1)
        v, se = ex.mc_integral(f, 0, 1, 10_000, random.Random(3))
        va, sea = ex.mc_integral_antithetic(f, 0, 1, 5_000, random.Random(3))
        self.assertLess(abs(v - exact), 3 * se)
        self.assertLess(abs(va - exact), 3 * sea)
        self.assertLess(sea, se / 3)
        self.assertEqual((round(ex.event_on_time_exact(), 4), ex.event_on_time(100_000, random.Random(4))), (0.7995, 0.79931))


if __name__ == "__main__":
    unittest.main()
