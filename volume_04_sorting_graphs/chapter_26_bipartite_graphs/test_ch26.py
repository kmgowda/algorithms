import unittest

import ch26_examples as ex


class TestChapter29(unittest.TestCase):
    def test_club(self) -> None:
        colour, cyc = ex.two_colour(ex.adjacency(ex.MEMBERS, ex.QUARRELS))
        self.assertIsNone(cyc)
        self.assertEqual(ex.teams(colour), (["Ana", "Cai", "Eva", "Gus"], ["Ben", "Dev", "Fay"]))
        for a, b in ex.QUARRELS:
            self.assertNotEqual(colour[a], colour[b])

    def test_odd_cycles(self) -> None:
        self.assertEqual(ex.two_colour(ex.adjacency(ex.MEMBERS, ex.QUARRELS + [("Ben", "Dev")]))[1],
                         ["Ben", "Ana", "Dev", "Ben"])
        cyc = ex.two_colour(ex.adjacency(ex.PLACES, ex.ROADS))[1]
        self.assertEqual(cyc, ["Market", "School", "Station", "Market"])

    def test_every_case(self) -> None:
        A = ex.adjacency
        square = ex.two_colour(A("ABCD", [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")]))[0]
        self.assertEqual((square["A"], square["C"], square["B"], square["D"]), (0, 0, 1, 1))
        five = ex.two_colour(A("ABCDE", [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"), ("E", "A")]))[1]
        self.assertEqual(len(five) - 1, 5)
        self.assertEqual(ex.two_colour(A("A", [("A", "A")]))[1], ["A", "A"])
        self.assertIsNotNone(ex.two_colour(A("ABCD", [("A", "B"), ("C", "D")]))[0])
        self.assertEqual(ex.two_colour(A("ABCD", [("A", "B"), ("A", "C"), ("A", "D")]))[0], {"A": 0, "B": 1, "C": 1, "D": 1})
        self.assertEqual(ex.two_colour(A("A", []))[0], {"A": 0})
        self.assertEqual(ex.two_colour({})[0], {})


if __name__ == "__main__":
    unittest.main()
