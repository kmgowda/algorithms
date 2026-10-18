import random
import string
import unittest

import ch04_examples as ex
import ch04_solutions as sol


class TestCharacters(unittest.TestCase):
    def test_code_points_and_utf8(self) -> None:
        self.assertEqual(ex.code_points("Zoo"), [90, 111, 111])
        self.assertEqual(ex.utf8_size("zebra"), (5, 5))
        self.assertEqual(ex.utf8_size("Zoë"), (3, 4))
        self.assertEqual(ex.utf8_size("动物园"), (3, 9))
        self.assertEqual(ex.utf8_size("🦁"), (1, 4))

    def test_caesar_round_trip(self) -> None:
        rng = random.Random(1)
        for _ in range(100):
            text = "".join(rng.choice(string.ascii_letters + " !,") for _ in range(30))
            shift = rng.randint(-30, 30)
            self.assertEqual(ex.caesar_shift(ex.caesar_shift(text, shift), -shift), text)
        self.assertEqual(ex.caesar_shift("xyz ABC", 3), "abc DEF")


class TestBuilding(unittest.TestCase):
    def test_builder(self) -> None:
        sb = ex.StringBuilder().add("Hello").add(", ").add("zoo")
        self.assertEqual(sb.build(), "Hello, zoo")
        self.assertEqual(len(sb), 10)

    def test_receipt(self) -> None:
        text = ex.receipt([("Mango", 3, 40.0), ("Milk", 2, 30.25)])
        self.assertTrue(text.endswith("180.50\n"))
        self.assertEqual(len(text.splitlines()), 3)


class TestProblems(unittest.TestCase):
    def test_reverse_words(self) -> None:
        self.assertEqual(ex.reverse_words("  the  quick brown   fox "), "fox brown quick the")
        self.assertEqual(ex.reverse_words(""), "")

    def test_prefix(self) -> None:
        self.assertEqual(ex.longest_common_prefix(["flower", "flow", "flight"]), "fl")
        self.assertEqual(ex.longest_common_prefix(["dog", "racecar"]), "")
        self.assertEqual(ex.longest_common_prefix([]), "")
        self.assertEqual(ex.longest_common_prefix(["solo"]), "solo")

    def test_palindrome(self) -> None:
        for word in ("", "a", "noon", "racecar", "zebra", "ab"):
            self.assertEqual(ex.is_palindrome_two_pointers(word), word == word[::-1])

    def test_industry(self) -> None:
        self.assertEqual(ex.normalize_username(" ZOË "), ex.normalize_username("zoe\u0308"))
        self.assertEqual(ex.normalize_username("Straße"), ex.normalize_username("STRASSE"))
        self.assertEqual(ex.mask_card_number("4111 1111 1111 1234"), "**** **** **** 1234")
        with self.assertRaises(ValueError):
            ex.mask_card_number("12")


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        self.assertTrue(sol.is_rotation("lion", "onli"))
        self.assertFalse(sol.is_rotation("lion", "loin"))
        self.assertFalse(sol.is_rotation("ab", "aba"))
        self.assertEqual(sol.run_length_decode("a3b1c12"), "aaab" + "c" * 12)
        self.assertEqual(sol.run_length_decode(""), "")
        self.assertEqual(sol.count_character_types("Bus 42 leaves!"),
                         {"letters": 9, "digits": 2, "spaces": 2, "other": 1})
        self.assertEqual(sol.slugify("Top 10 Zoo Animals!"), "top-10-zoo-animals")
        self.assertEqual(sol.slugify("  --  "), "")
        lines = sol.wrap_text("the quick brown fox jumps over the lazy dog", 10)
        self.assertEqual(lines, ["the quick", "brown fox", "jumps over", "the lazy", "dog"])
        self.assertTrue(all(len(line) <= 10 for line in lines))


if __name__ == "__main__":
    unittest.main()
