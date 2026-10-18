import unittest

import ch08_examples as ex
import ch08_solutions as sol


class TestStrings(unittest.TestCase):
    def test_tour(self) -> None:
        result = ex.string_tour("My cats love the city zoo")
        self.assertEqual(result["words"], ["My", "cats", "love", "the", "city", "zoo"])
        self.assertTrue(result["has_zoo"])
        self.assertEqual(result["position_of_zoo"], 22)
        self.assertEqual(result["replaced"], "My dogs love the city zoo")
        self.assertEqual(result["initials"], "MCLTCZ")
        self.assertEqual(ex.string_tour("")["first_word"], "")

    def test_palindrome_username(self) -> None:
        self.assertTrue(ex.is_palindrome("Was it a car or a cat I saw?"))
        self.assertTrue(ex.is_palindrome(""))
        self.assertFalse(ex.is_palindrome("zoo"))
        self.assertEqual(ex.make_username("  Maya Rao ", 2012), "maya.rao2012")


class TestDictionaries(unittest.TestCase):
    def test_sounds(self) -> None:
        self.assertEqual(ex.animal_sounds_demo(), {"dog": "bark", "cat": "meow", "duck": "quack"})

    def test_frequencies(self) -> None:
        story = "The lion saw the zebra. The zebra saw the lion and ran!"
        counts = ex.word_frequencies(story)
        self.assertEqual(counts["the"], 4)
        self.assertEqual(counts["zebra"], 2)
        self.assertEqual(counts["ran"], 1)
        self.assertEqual(ex.most_common_word(story), "the")
        self.assertIsNone(ex.most_common_word(""))

    def test_grouping(self) -> None:
        self.assertEqual(ex.group_by_first_letter(["Ana", "Ben", "Alex", "Bea", "Cy"]),
                         {"A": ["Ana", "Alex"], "B": ["Ben", "Bea"], "C": ["Cy"]})

    def test_restock(self) -> None:
        report = ex.restock_report({"milk": 20, "bread": 8, "eggs": 30}, {"milk": 17, "eggs": 5})
        self.assertEqual(report, ["milk: 3 left"])
        self.assertEqual(ex.restock_report({"tea": 2}, {}), ["tea: 2 left"])


class TestSets(unittest.TestCase):
    def test_sets(self) -> None:
        self.assertEqual(ex.unique_visitors(["ana", "ben", "ana", "cy", "ben"]), 3)
        self.assertFalse(ex.is_username_available({"maya", "leo"}, "Maya"))
        self.assertTrue(ex.is_username_available({"maya", "leo"}, "Priya"))
        self.assertEqual(ex.mutual_friends({"Ana", "Ben", "Cy"}, {"Ben", "Cy", "Dev"}), {"Ben", "Cy"})

    def test_clubs(self) -> None:
        result = ex.club_overview({"Ana", "Ben", "Cy"}, {"Cy", "Dev"})
        self.assertEqual(result["both"], {"Cy"})
        self.assertEqual(result["either"], {"Ana", "Ben", "Cy", "Dev"})
        self.assertEqual(result["only_chess"], {"Ana", "Ben"})
        self.assertEqual(result["exactly_one"], {"Ana", "Ben", "Dev"})


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        self.assertEqual(sol.count_vowels_by_letter("Elephant and Iguana"),
                         {"a": 4, "e": 2, "i": 1, "o": 0, "u": 1})
        self.assertTrue(sol.are_anagrams("Listen", "Silent"))
        self.assertTrue(sol.are_anagrams("Dormitory", "Dirty room"))
        self.assertFalse(sol.are_anagrams("aab", "abb"))
        self.assertEqual(sol.title_case("the jungle BOOK"), "The Jungle Book")
        self.assertEqual(sol.invert_phone_book({"Ana": "555-01"}), {"555-01": "Ana"})
        self.assertEqual(sol.first_repeated(["lion", "zebra", "otter", "zebra"]), "zebra")
        self.assertIsNone(sol.first_repeated(["a", "b"]))
        self.assertEqual(sol.compress("aaabccdddd"), "a3b1c2d4")
        self.assertEqual(sol.compress(""), "")
        self.assertEqual(sol.compress("z"), "z1")
        self.assertEqual(sol.books_due({"Matilda": 10, "Holes": 14, "Wonder": 9}, 11), ["Matilda", "Wonder"])


if __name__ == "__main__":
    unittest.main()
