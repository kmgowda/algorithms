import random
import sys
import unittest

import ch08_examples as ex
import ch08_solutions as sol


class TestCallStack(unittest.TestCase):
    def test_trace(self) -> None:
        result, trace = ex.factorial_traced(3)
        self.assertEqual(result, 6)
        self.assertEqual(trace[0], "call factorial(3)")
        self.assertEqual(trace[3], "            call factorial(0)")
        self.assertEqual(trace[-1], "return 6")
        self.assertEqual(len(trace), 8)

    def test_recursion_limit(self) -> None:
        depth = ex.deepest_recursion_possible()
        self.assertGreater(depth, 100)
        self.assertLessEqual(depth, sys.getrecursionlimit())

    def test_stack_trace(self) -> None:
        self.assertEqual(ex.stack_trace_of_failure(),
                         ["stack_trace_of_failure", "checkout", "compute_total", "price_of"])


class TestRecursionTrees(unittest.TestCase):
    def test_fibonacci(self) -> None:
        self.assertEqual([ex.fibonacci_naive(n) for n in range(10)], [0, 1, 1, 2, 3, 5, 8, 13, 21, 34])
        for n in range(0, 20):
            self.assertEqual(ex.fibonacci_call_count(n), sol.fibonacci_calls_formula(n))
        self.assertEqual(ex.fibonacci_call_count(20), 21891)

    def test_levels(self) -> None:
        levels = ex.calls_per_level(6)
        self.assertEqual(levels[0], 1)
        self.assertEqual(levels[1], 2)
        self.assertEqual(sum(levels), ex.fibonacci_call_count(6))


class TestRewrites(unittest.TestCase):
    def test_sums(self) -> None:
        rng = random.Random(4)
        for _ in range(100):
            values = [rng.randint(-9, 9) for _ in range(rng.randint(0, 30))]
            self.assertEqual(ex.sum_from(values), sum(values))
            self.assertEqual(ex.sum_with_accumulator(values), sum(values))

    def test_folders(self) -> None:
        disk = {"files": {"a": 4}, "folders": {"b": {"files": {"c": 10}, "folders": {
            "d": {"files": {"e": 1, "f": 2}, "folders": {}}}}}}
        self.assertEqual(ex.folder_size_recursive(disk), 17)
        self.assertEqual(ex.folder_size_iterative(disk), 17)
        self.assertEqual(sol.count_files_iterative(disk), 4)
        self.assertEqual(sorted(sol.all_paths(disk)), ["a", "b/c", "b/d/e", "b/d/f"])

    def test_deep_data(self) -> None:
        self.assertEqual(ex.nesting_depth_iterative(ex.make_deep_list(5000)), 5000)
        self.assertEqual(ex.nesting_depth_iterative({"a": [1, {"b": []}]}), 4)   # dict > list > dict > list
        self.assertEqual(ex.nesting_depth_iterative({"a": 1}), 1)
        self.assertEqual(ex.nesting_depth_iterative(42), 0)


class TestSolutions(unittest.TestCase):
    def test_misc(self) -> None:
        self.assertEqual(sol.max_stack_depth_of_countdown(5), 6)
        self.assertEqual(sol.reverse_from("zebra"), "arbez")
        self.assertEqual(sol.reverse_from(""), "")
        self.assertEqual(sol.binary_strings(2), ["00", "01", "10", "11"])
        self.assertEqual(len(sol.binary_strings(10)), 1024)


if __name__ == "__main__":
    unittest.main()
