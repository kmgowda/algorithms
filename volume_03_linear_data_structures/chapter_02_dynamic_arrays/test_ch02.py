import random
import unittest

import ch02_examples as ex
import ch02_solutions as sol
from ch02_examples import DynamicArray


class TestDynamicArray(unittest.TestCase):
    def test_basic(self) -> None:
        a = DynamicArray(capacity=2)
        for x in "abcde":
            a.append(x)
        self.assertEqual(list(a), list("abcde"))
        self.assertEqual((len(a), a.capacity, a.copies), (5, 8, 2 + 4))
        self.assertEqual((a[0], a[-1]), ("a", "e"))
        a[1] = "B"
        self.assertEqual(a[1], "B")
        with self.assertRaises(IndexError):
            a[5]
        with self.assertRaises(IndexError):
            a[-6] = "x"
        with self.assertRaises(ValueError):
            DynamicArray(0)

    def test_against_python_list(self) -> None:
        rng = random.Random(7)
        mine, model = DynamicArray(), []
        for _ in range(5000):
            op = rng.random()
            if op < 0.4:
                v = rng.randint(0, 20)
                mine.append(v)
                model.append(v)
            elif op < 0.6:
                i = rng.randint(0, len(model))
                v = rng.randint(0, 20)
                mine.insert(i, v)
                model.insert(i, v)
            elif op < 0.85 and model:
                i = rng.randrange(-len(model), len(model))
                self.assertEqual(mine.pop(i), model.pop(i))
            elif model:
                v = rng.choice(model)
                mine.remove(v)
                model.remove(v)
            self.assertEqual(list(mine), model)
            self.assertLessEqual(len(mine), mine.capacity)

    def test_search_and_errors(self) -> None:
        a = DynamicArray()
        sol.extend(a, ["x", "y", "z"])
        self.assertEqual(a.index("y"), 1)
        self.assertIn("z", a)
        self.assertNotIn("w", a)
        with self.assertRaises(ValueError):
            a.remove("w")
        with self.assertRaises(ValueError):
            a.index("w")
        with self.assertRaises(IndexError):
            a.insert(9, "q")
        self.assertIn("capacity=", repr(a))

    def test_amortized_and_shrinking(self) -> None:
        log = ex.sensor_log([float(i) for i in range(1000)])
        self.assertLess(log.copies, 2 * 1000)
        sol.clear(log)
        self.assertEqual(len(log), 0)
        self.assertLessEqual(log.capacity, 8)

    def test_boarding(self) -> None:
        self.assertEqual(ex.boarding_order(["Ana", "Ben"], ["W", "F"]), ["W", "F", "Ana", "Ben"])


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        a = DynamicArray()
        sol.extend(a, [1, 2, 3, 2, 2])
        sol.reverse_in_place(a)
        self.assertEqual(list(a), [2, 2, 3, 2, 1])
        self.assertEqual(sol.count_value(a, 2), 3)
        self.assertEqual(sol.remove_all(a, 2), 3)
        self.assertEqual(list(a), [3, 1])
        empty = DynamicArray()
        sol.reverse_in_place(empty)
        self.assertEqual(list(empty), [])


if __name__ == "__main__":
    unittest.main()
