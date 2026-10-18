import unittest

from ch01_examples import atm_withdraw, bus_or_walk, delivery_eta, find_book_shelf, lemonade_steps
from ch01_solutions import brush_teeth_steps, elevator_direction, is_precise, traffic_light_action


class TestExamples(unittest.TestCase):
    def test_lemonade_scales_with_glasses(self) -> None:
        steps = lemonade_steps(3)
        self.assertEqual(steps[0], "Take 6 lemons.")
        self.assertEqual(steps[-1], "Pour into 3 glasses.")
        self.assertEqual(lemonade_steps(0), ["Nothing to make."])

    def test_bus_or_walk(self) -> None:
        self.assertEqual(bus_or_walk(5, 20), "Take the bus")
        self.assertEqual(bus_or_walk(20, 26), "Walk")
        self.assertEqual(bus_or_walk(15, 20), "Call a parent for a ride")

    def test_atm(self) -> None:
        self.assertEqual(atm_withdraw(1000, True, 300), ("Please take your 300.", 700))
        self.assertEqual(atm_withdraw(1000, False, 300)[1], 1000)
        self.assertEqual(atm_withdraw(100, True, 300)[0], "Insufficient funds.")
        self.assertEqual(atm_withdraw(1000, True, 150)[1], 1000)

    def test_library_shelf(self) -> None:
        self.assertEqual(find_book_shelf("Animal Farm"), "Shelf 1")
        self.assertEqual(find_book_shelf("jungle book"), "Shelf 2")
        self.assertEqual(find_book_shelf("Zebra Tales"), "Shelf 3")
        self.assertEqual(find_book_shelf("1984"), "Ask the librarian")

    def test_delivery_eta(self) -> None:
        self.assertEqual(delivery_eta(4, 20, 15), 27)
        with self.assertRaises(ValueError):
            delivery_eta(4, 0, 15)


class TestSolutions(unittest.TestCase):
    def test_brushing_is_precise_and_finite(self) -> None:
        steps = brush_teeth_steps()
        self.assertTrue(0 < len(steps) < 20)
        self.assertTrue(all(is_precise(step) for step in steps))

    def test_vague_detection(self) -> None:
        self.assertFalse(is_precise("Add some sugar"))
        self.assertTrue(is_precise("Add 2 spoons of sugar"))

    def test_traffic_light(self) -> None:
        self.assertEqual(traffic_light_action("RED"), "Stop")
        self.assertEqual(traffic_light_action("blue"), "Treat as a stop sign")

    def test_elevator(self) -> None:
        self.assertEqual(elevator_direction(3, 7), "Up")
        self.assertEqual(elevator_direction(7, 3), "Down")
        self.assertEqual(elevator_direction(4, 4), "Open doors")


if __name__ == "__main__":
    unittest.main()
