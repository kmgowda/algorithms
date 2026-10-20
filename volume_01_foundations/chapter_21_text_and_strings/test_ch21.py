import random
import unittest

import ch21_examples as ex


class TestChapter21(unittest.TestCase):
    def test_search(self) -> None:
        rng = random.Random(1)
        for _ in range(500):
            text = "".join(rng.choice("ab") for _ in range(rng.randint(0, 15)))
            word = "".join(rng.choice("ab") for _ in range(rng.randint(1, 3)))
            expected = [i for i in range(len(text) - len(word) + 1) if text[i:i + len(word)] == word]
            self.assertEqual(ex.find_all(text, word), expected)
        self.assertEqual(ex.find_all("a map of maps", "map"), [2, 9])
        self.assertEqual(ex.find_all("banana", "ana"), [1, 3])

    def test_strings(self) -> None:
        self.assertTrue(ex.is_palindrome("RACECAR"))
        self.assertTrue(ex.is_palindrome("neveroddoreven"))
        self.assertFalse(ex.is_palindrome("BOOKS"))
        self.assertTrue(ex.is_palindrome(""))
        self.assertEqual(ex.copies_with_plus(["x" * 5] * 100), 25_250)
        self.assertEqual(ex.copies_with_plus(["x" * 10] * 200), 201_000)
        self.assertEqual(ex.build_newsletter(["ab", "cd"]), "abcd")
        self.assertEqual([ord(c) for c in "Ca0"], [67, 97, 48])
        self.assertEqual(ex.letter_counts("Maya"), {"m": 1, "a": 2, "y": 1})


if __name__ == "__main__":
    unittest.main()
