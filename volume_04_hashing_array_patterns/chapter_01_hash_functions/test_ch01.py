import random
import string
import unittest

import ch01_examples as ex
import ch01_solutions as sol


class TestHashFunctions(unittest.TestCase):
    def test_range_and_determinism(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            key = "".join(rng.choice(string.ascii_lowercase) for _ in range(rng.randint(0, 10)))
            for fn in (ex.first_letter_hash, ex.sum_of_codes_hash, ex.polynomial_hash):
                h = fn(key, 13)
                self.assertTrue(0 <= h < 13)
                self.assertEqual(h, fn(key, 13))

    def test_weaknesses(self) -> None:
        self.assertEqual(ex.first_letter_hash("lion", 13), ex.first_letter_hash("llama", 13))
        self.assertEqual(ex.sum_of_codes_hash("listen", 13), ex.sum_of_codes_hash("silent", 13))
        self.assertNotEqual(ex.polynomial_hash("listen", 1009), ex.polynomial_hash("silent", 1009))

    def test_polynomial_spreads_better(self) -> None:
        bad = ex.spread_report(ex.ANIMALS, 13, ex.first_letter_hash)
        good = ex.spread_report(ex.ANIMALS, 13, ex.polynomial_hash)
        self.assertLess(good["max_in_one_slot"], bad["max_in_one_slot"])
        self.assertEqual(sum(ex.bucket_counts(ex.ANIMALS, 13, ex.polynomial_hash)), len(ex.ANIMALS))

    def test_avalanche(self) -> None:
        self.assertGreater(ex.avalanche_demo("lion", "lioN"), 80)
        self.assertEqual(ex.avalanche_demo("lion", "lion"), 0)

    def test_files_and_passwords(self) -> None:
        photos = {"a.jpg": b"same", "b.jpg": b"same", "c.jpg": b"other", "d.jpg": b"other", "e.jpg": b"x"}
        self.assertEqual(ex.find_duplicate_files(photos), [["a.jpg", "b.jpg"], ["c.jpg", "d.jpg"]])
        salt, stored = ex.hash_password("zebra-stripes", b"0123456789abcdef")
        self.assertTrue(ex.check_password("zebra-stripes", salt, stored))
        self.assertFalse(ex.check_password("zebra", salt, stored))
        _, other = ex.hash_password("zebra-stripes", b"fedcba9876543210")
        self.assertNotEqual(stored, other)          # different salt, different hash


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        self.assertEqual(sol.hash_by_hand("cat", 101), [99 % 101, (99 * 31 + 97) % 101, ((99 * 31 + 97) * 31 + 116) % 101])
        self.assertEqual(sol.hash_by_hand("cat", 101)[-1], ex.polynomial_hash("cat", 101))
        self.assertEqual(sol.phone_hash("+91 80 4123 5678", 100), 78)
        self.assertEqual(sol.collisions(["a", "b", "c", "k"], 10), 1)   # 'a'=97 and 'k'=107 share slot 7
        self.assertNotEqual(sol.tuple_hash((1, 2), 97), sol.tuple_hash((2, 1), 97))
        self.assertAlmostEqual(sol.birthday_probability(23), 0.507, places=3)
        self.assertEqual(sol.birthday_probability(1), 0.0)


if __name__ == "__main__":
    unittest.main()
