import random
import unittest

import ch21_examples as ex


class TestChapter21(unittest.TestCase):
    def test_every_case(self) -> None:
        self.assertEqual(ex.find_all("banana", "ana"), [1, 3])
        self.assertEqual(ex.find_all("a map of maps", "map"), [2, 9])
        self.assertEqual((ex.find_all("maps", "zebra"), ex.find_all("Map", "map"), ex.find_all("map", "map")), ([], [], [0]))
        self.assertEqual(ex.find_all("maps", ""), [0, 1, 2, 3, 4])
        self.assertEqual([ex.is_palindrome(w) for w in ("", "a", "abba", "RaceCar", "race car", "books")],
                         [True, True, True, True, False, False])
        self.assertEqual((ex.letter_counts(""), ex.letter_counts("A a!")), ({}, {"a": 2}))
        self.assertEqual((ex.copies_with_plus([]), ex.copies_with_plus(["abc"]), ex.copies_with_plus(["x" * 10] * 200)),
                         (0, 3, 201000))

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
