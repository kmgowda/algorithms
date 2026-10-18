import unittest

from ch07_examples import (
    aliasing_demo,
    attendance_report,
    count_meals,
    departures_board,
    feeding_grid,
    fruit_basket_demo,
    playlist_after_actions,
    squares_up_to,
    stops_between,
)
from ch07_solutions import (
    cart_total,
    column,
    remove_all,
    reverse_in_place,
    reverse_list,
    rotate_queue,
    total_of,
)


class TestExamples(unittest.TestCase):
    def test_basket(self) -> None:
        result = fruit_basket_demo()
        self.assertEqual(result["first"], "apple")
        self.assertEqual(result["last"], "cherry")
        self.assertEqual(result["basket"], ["apple", "kiwi", "cherry"])
        self.assertEqual(result["popped"], "mango")
        self.assertTrue(result["has_kiwi"])
        self.assertEqual(result["size"], 3)

    def test_attendance(self) -> None:
        self.assertEqual(attendance_report(["Ana", "Ben", "Cy", "Dev"], ["Ben", "Dev"]), ["Ana", "Cy"])
        self.assertEqual(attendance_report([], ["Ben"]), [])

    def test_route(self) -> None:
        route = ["Depot", "Library", "Market", "Hospital", "School"]
        self.assertEqual(stops_between(route, "Library", "Hospital"), ["Library", "Market", "Hospital"])
        self.assertEqual(stops_between(route, "Hospital", "Library"), ["Hospital", "Market", "Library"])
        self.assertEqual(stops_between(route, "Market", "Market"), ["Market"])

    def test_grid(self) -> None:
        self.assertEqual(count_meals(feeding_grid(), "fish"), 6)
        self.assertEqual(count_meals(feeding_grid(), "krill"), 1)

    def test_playlist(self) -> None:
        original = ["Song A", "Song B"]
        result = playlist_after_actions(original, [("add", "Song C"), ("play_next", "Song Z"), ("skip", "")])
        self.assertEqual(result, ["Song A", "Song B", "Song C"])
        self.assertEqual(original, ["Song A", "Song B"])
        self.assertEqual(playlist_after_actions([], [("skip", ""), ("remove", "X")]), [])

    def test_departures(self) -> None:
        flights = [("AI202", "Delhi", 1430), ("BA118", "London", 915), ("EK501", "Dubai", 1105)]
        self.assertEqual(departures_board(flights, 1000), ["1105 EK501 to Dubai", "1430 AI202 to Delhi"])
        self.assertEqual(departures_board(flights, 0)[0], "0915 BA118 to London")

    def test_alias(self) -> None:
        original, alias, copy = aliasing_demo()
        self.assertIs(original, alias)
        self.assertEqual(original, ["lion", "tiger", "bear"])
        self.assertEqual(copy, ["lion", "tiger"])

    def test_comprehension(self) -> None:
        self.assertEqual(squares_up_to(5), [1, 4, 9, 16, 25])


class TestSolutions(unittest.TestCase):
    def test_total_and_reverse(self) -> None:
        self.assertEqual(total_of([2.5, 3, 4.5]), 10.0)
        self.assertEqual(total_of([]), 0.0)
        self.assertEqual(reverse_list(["a", "b", "c"]), ["c", "b", "a"])
        self.assertEqual(reverse_list([]), [])

    def test_reverse_in_place(self) -> None:
        for items in (["a", "b", "c", "d"], ["a", "b", "c"], ["a"], []):
            expected = items[::-1]
            reverse_in_place(items)
            self.assertEqual(items, expected)

    def test_rotate(self) -> None:
        self.assertEqual(rotate_queue(["Ana", "Ben", "Cy"], 1), ["Ben", "Cy", "Ana"])
        self.assertEqual(rotate_queue(["Ana", "Ben", "Cy"], 4), ["Ben", "Cy", "Ana"])
        self.assertEqual(rotate_queue([], 3), [])

    def test_grid_cart_remove(self) -> None:
        self.assertEqual(column([[1, 2], [3, 4]], 1), [2, 4])
        self.assertEqual(cart_total([10.0, 2.5], [3, 4]), 40.0)
        with self.assertRaises(ValueError):
            cart_total([1.0], [1, 2])
        self.assertEqual(remove_all(["cat", "dog", "cat"], "cat"), ["dog"])


if __name__ == "__main__":
    unittest.main()
