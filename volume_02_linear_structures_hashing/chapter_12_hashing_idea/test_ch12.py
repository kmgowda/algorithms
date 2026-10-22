import random
import unittest

import ch12_examples as ex


class TestChapter30(unittest.TestCase):
    def test_every_case(self) -> None:
        self.assertEqual((ex.letter_sum_hash("", 8), ex.multiply_add_hash("", 8)), (0, 0))
        self.assertEqual((ex.letter_sum_hash("ART", 8), ex.letter_sum_hash("RAT", 8)), (7, 7))
        self.assertEqual((ex.multiply_add_hash("ART", 8), ex.multiply_add_hash("RAT", 8)), (3, 5))
        self.assertEqual((ex.letter_sum_hash("MAYA", 1), ex.multiply_add_hash("MAYA", 1)), (0, 0))
        self.assertEqual((ex.letter_sum_hash("Maya", 8), ex.letter_sum_hash("MAYA", 8)), (0, 0))
        self.assertEqual([ex.duplicates_hashed(a) for a in ([], [7], [5, 5, 5], [1, 2, 3])],
                         [(set(), 0), (set(), 1), ({5}, 3), (set(), 3)])
        self.assertEqual((ex.birthday_shared(1), ex.birthday_shared(366, trials=200)), (0.0, 1.0))
        self.assertAlmostEqual(ex.birthday_shared(23), 0.5, delta=0.03)

    def test_hashes(self) -> None:
        self.assertEqual(ex.letter_sum_hash("MAYA", 8), 0)
        self.assertEqual(ex.letter_sum_hash("BEN", 8), 5)
        self.assertEqual([ex.letter_sum_hash(n, 8) for n in ["Maya", "Ravi", "Ana", "Ben", "Leo", "Zoe"]],
                         [0, 2, 0, 5, 0, 6])
        self.assertEqual((ex.multiply_add_hash("AB", 8), ex.multiply_add_hash("BA", 8)), (1, 7))
        for k in ("x", "hello", "library"):
            self.assertEqual(ex.multiply_add_hash(k, 101), ex.multiply_add_hash(k, 101))

    def test_duplicates(self) -> None:
        rng = random.Random(1)
        for _ in range(50):
            day = [rng.randint(1, 60) for _ in range(rng.randint(0, 40))]
            self.assertEqual(ex.duplicates_pairwise(day)[0], ex.duplicates_hashed(day)[0])
        self.assertEqual(ex.duplicates_pairwise(list(range(500)))[1], 124_750)
        self.assertGreater(ex.birthday_shared(23, trials=5000), 0.45)


if __name__ == "__main__":
    unittest.main()
