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


if __name__ == "__main__":
    unittest.main()
