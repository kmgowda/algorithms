import random
import unittest

import ch14_examples as ex


class TestChapter14(unittest.TestCase):
    def test_sorts(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            a = [rng.randint(0, 40) for _ in range(rng.randint(0, 40))]
            b = list(a)
            ex.heapsort(b)
            self.assertEqual(b, sorted(a))

    def test_examples(self) -> None:
        a, c, log = list(ex.PILE), {"comparisons": 0}, []
        ex.heapsort(a, c, log)
        self.assertEqual(c["comparisons"], 29)
        self.assertEqual(log[0], ("heap", [91, 70, 84, 63, 25, 47, 58, 31, 12]))
        self.assertEqual(log[1], (91, [84, 70, 58, 63, 25, 47, 12, 31, 91]))
        rng = random.Random(1)
        x = [rng.randint(0, 10 ** 6) for _ in range(5000)]
        self.assertEqual(ex.top_k_by_heapsort(x, 10), sorted(x, reverse=True)[:10])


if __name__ == "__main__":
    unittest.main()
