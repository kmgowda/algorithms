import random
import unittest

import ch16_examples as ex
import ch16_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_smallest_inputs(self) -> None:
        self.assertEqual(sol.titles_by_popularity([]), [])
        self.assertEqual(sol.titles_by_popularity(["Maps"]), ["Maps"])
        self.assertEqual(sol.titles_by_popularity(["Maps", "Maps"]), ["Maps"])

    def test_chapter_loans_and_ties(self) -> None:
        self.assertEqual(sol.titles_by_popularity(["Maps", "Ocean", "Maps", "Clocks", "Maps", "Ocean"]),
                         ["Maps", "Ocean", "Clocks"])
        self.assertEqual(sol.titles_by_popularity(["b", "a", "c"]), ["b", "a", "c"])

    def test_against_a_sort(self) -> None:
        rng = random.Random(16)
        for _ in range(300):
            loans = [rng.choice("abcdefg") for _ in range(rng.randint(0, 25))]
            counts = ex.count_loans(loans)
            first = {t: loans.index(t) for t in counts}
            self.assertEqual(sol.titles_by_popularity(loans), sorted(counts, key=lambda t: (-counts[t], first[t])))

    def test_shared_list_bug(self) -> None:
        books = [("Lucas", "Hanoi"), ("Polya", "How to Solve It")]
        bad = sol.group_by_author_buggy(books)
        self.assertEqual(bad["Lucas"], ["Hanoi", "How to Solve It"])
        self.assertIs(bad["Lucas"], bad["Polya"])
        self.assertEqual(ex.group_by(books, key=lambda b: b[0])["Lucas"], [("Lucas", "Hanoi")])
        self.assertEqual(sol.group_by_author_buggy([]), {})


if __name__ == "__main__":
    unittest.main()
