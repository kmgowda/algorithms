import contextlib
import io
import unittest

from ch02_examples import FRUIT_SHOP_PROGRAM, first_program, run_tiny_computer, to_binary
from ch02_solutions import binary_to_decimal, bytes_for_photos, seconds_in_a_week, where_to_keep


class TestExamples(unittest.TestCase):
    def test_first_program_output(self) -> None:
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            first_program()
        lines = buffer.getvalue().splitlines()
        self.assertEqual(lines[0], "Hello, World!")
        self.assertIn("2.5", lines)
        self.assertIn("1024", lines)
        self.assertEqual(lines[-1], "Seconds in one day: 86400")

    def test_to_binary(self) -> None:
        self.assertEqual(to_binary(0), "0")
        self.assertEqual(to_binary(13), "1101")
        with self.assertRaises(ValueError):
            to_binary(-1)

    def test_tiny_computer(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()):
            memory = run_tiny_computer(FRUIT_SHOP_PROGRAM)
        self.assertEqual(memory["fruits"], 8)
        self.assertEqual(memory["bill"], 160)

    def test_tiny_computer_sub_and_unknown(self) -> None:
        memory = run_tiny_computer([("SET", "a", "9"), ("SET", "b", "4"), ("SUB", "c", "a", "b")])
        self.assertEqual(memory["c"], 5)
        with self.assertRaises(ValueError):
            run_tiny_computer([("JUMP", "x")])


class TestSolutions(unittest.TestCase):
    def test_binary_round_trip(self) -> None:
        for number in range(200):
            self.assertEqual(binary_to_decimal(to_binary(number)), number)
        with self.assertRaises(ValueError):
            binary_to_decimal("102")

    def test_numbers(self) -> None:
        self.assertEqual(seconds_in_a_week(), 604800)
        self.assertEqual(bytes_for_photos(200, 3), 600_000_000)

    def test_where_to_keep(self) -> None:
        self.assertEqual(where_to_keep(True, True), "storage")
        self.assertEqual(where_to_keep(False, True), "memory")
        self.assertEqual(where_to_keep(False, False), "nowhere - delete it")


if __name__ == "__main__":
    unittest.main()
