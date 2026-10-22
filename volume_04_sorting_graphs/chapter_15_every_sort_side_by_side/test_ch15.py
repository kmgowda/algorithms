import random
import unittest

import ch15_examples as ex

CASES = [ex.PILE, sorted(ex.PILE), sorted(ex.PILE, reverse=True), [47] * 9, [58, 25, 58, 12, 25, 47, 58, 12, 47], [47], []]
MATRIX = {"selection": [36, 36, 36, 36, 36, 0, 0], "insertion": [23, 8, 36, 8, 23, 0, 0],
          "bubble": [33, 8, 36, 8, 35, 0, 0], "merge": [21, 13, 16, 13, 20, 0, 0], "heap": [29, 35, 30, 21, 29, 0, 0],
          "Timsort (teaching)": [27, 8, 8, 8, 23, 0, 0]}


class TestChapter21(unittest.TestCase):
    def test_all_sort_correctly(self) -> None:
        rng = random.Random(1)
        for _ in range(20):
            data = [rng.randrange(500) for _ in range(rng.randint(0, 120))]
            ex.run_all(data)                    # run_all asserts every result is sorted

    def test_every_case_matrix(self) -> None:
        for name, row in MATRIX.items():
            got = [ex.SORTS[name](list(a))[1] for a in CASES]
            self.assertEqual(got, row, name)

    def test_quadratic_counts(self) -> None:
        rng = random.Random(1)
        data = [rng.randrange(1_000_000) for _ in range(500)]
        r = ex.run_all(data)
        self.assertEqual(r["selection"][0], 500 * 499 // 2)
        self.assertLess(r["merge"][0], r["insertion"][0])


if __name__ == "__main__":
    unittest.main()
