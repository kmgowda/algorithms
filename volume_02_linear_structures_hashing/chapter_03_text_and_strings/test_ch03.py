import random
import unittest

import ch03_examples as ex


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

    def test_compare(self) -> None:
        self.assertEqual(ex.compare("map", "maps"), (-1, 3))
        self.assertEqual(ex.compare("Maya", "maya"), (-1, 1))
        self.assertEqual(ex.compare("library", "librarian"), (1, 7))
        self.assertEqual(ex.compare("", ""), (0, 0))
        self.assertEqual(ex.compare("", "a"), (-1, 0))
        self.assertEqual(ex.compare("map", "map"), (0, 3))
        rng = random.Random(2)
        for _ in range(300):
            a = "".join(rng.choice("abC") for _ in range(rng.randint(0, 5)))
            b = "".join(rng.choice("abC") for _ in range(rng.randint(0, 5)))
            self.assertEqual(ex.compare(a, b)[0], (a > b) - (a < b))
            self.assertLessEqual(ex.compare(a, b)[1], min(len(a), len(b)))

    def test_substrings_and_subsequences(self) -> None:
        self.assertEqual(ex.substrings("MAP"), ["M", "MA", "MAP", "A", "AP", "P"])
        self.assertEqual(ex.subsequences("MAP"), ["MAP", "MA", "MP", "M", "AP", "A", "P", ""])
        self.assertEqual((ex.substrings(""), ex.subsequences("")), ([], [""]))
        for n in range(0, 9):
            text = "abcdefgh"[:n]
            self.assertEqual(len(ex.substrings(text)), n * (n + 1) // 2)
            self.assertEqual(len(ex.subsequences(text)), 2 ** n)
        self.assertEqual((len(ex.substrings("LIBRARY")), len(ex.subsequences("LIBRARY"))), (28, 128))

    def test_utf8(self) -> None:
        self.assertEqual(ex.utf8_lengths("café 😀"), [1, 1, 1, 2, 1, 4])
        self.assertEqual(ex.utf8_lengths(""), [])
        self.assertEqual((len("café"), len("café".encode("utf-8"))), (4, 5))


if __name__ == "__main__":
    unittest.main()
