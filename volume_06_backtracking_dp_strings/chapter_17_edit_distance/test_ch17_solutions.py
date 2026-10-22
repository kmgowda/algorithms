import random
import unittest

import ch17_examples as ex
import ch17_solutions as sol


class TestChapter17Solutions(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual((sol.within_distance("PEOMS", "POEMS", 2), sol.within_distance("PEOMS", "POEMS", 1)), (2, None))
        self.assertEqual(sol.within_distance("KITTEN", "SITTING", 3), 3)
        self.assertIsNone(sol.within_distance("KITTEN", "SITTING", 2))

    def test_smallest(self) -> None:
        self.assertEqual(sol.within_distance("", "", 0), 0)
        self.assertEqual(sol.within_distance("A", "A", 0), 0)
        self.assertIsNone(sol.within_distance("A", "B", 0))
        self.assertIsNone(sol.within_distance("", "AB", 1))
        self.assertEqual(sol.within_distance("", "AB", 2), 2)
        self.assertEqual(sol.within_distance("AB", "", 5), 2)
        self.assertIsNone(sol.within_distance("A", "A", -1))

    def test_random_against_full_table(self) -> None:
        r = random.Random(17)
        for _ in range(500):
            a = "".join(r.choice("AB") for _ in range(r.randint(0, 8)))
            b = "".join(r.choice("ABC") for _ in range(r.randint(0, 8)))
            k = r.randint(0, 6)
            d = ex.edit_distance(a, b)[0]
            self.assertEqual(sol.within_distance(a, b, k), d if d <= k else None)
            self.assertLessEqual(sol.cells_filled(len(a), len(b), k), (len(a) + 1) * (2 * k + 1))


if __name__ == "__main__":
    unittest.main()
