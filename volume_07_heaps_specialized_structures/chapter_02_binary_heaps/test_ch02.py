import random
import unittest

import ch02_examples as ex
import ch02_solutions as sol


class TestMinHeap(unittest.TestCase):
    def test_against_model(self) -> None:
        rng = random.Random(1)
        h, model = ex.MinHeap(), {}
        next_id = 0
        for _ in range(4000):
            op = rng.random()
            if op < 0.4 or not model:
                h.push(next_id, rng.randint(0, 50))
                model[next_id] = h._data[h._where[next_id]][0]
                next_id += 1
            elif op < 0.6:
                item = rng.choice(list(model))
                p = rng.randint(0, 50)
                h.change_priority(item, p)
                model[item] = p
            elif op < 0.75:
                item = rng.choice(list(model))
                h.remove(item)
                del model[item]
            else:
                item, p = h.pop()
                self.assertEqual(p, min(model.values()))
                self.assertEqual(model.pop(item), p)
            self.assertTrue(h.is_valid())
            self.assertEqual(len(h), len(model))
        with self.assertRaises(IndexError):
            ex.MinHeap().pop()
        h2 = ex.MinHeap()
        h2.push("a", 1)
        with self.assertRaises(KeyError):
            h2.push("a", 2)
        self.assertIn("a", h2)
        self.assertEqual(h2.peek(), ("a", 1))

    def test_heapify(self) -> None:
        rng = random.Random(2)
        for _ in range(200):
            v = [rng.randint(0, 99) for _ in range(rng.randint(0, 40))]
            a = ex.heapify(v)
            self.assertTrue(sol.is_min_heap(a))
            self.assertEqual(sorted(a), sorted(v))

    def test_ride_hailing(self) -> None:
        self.assertEqual(ex.ride_hailing([("Ana", 2.5), ("Ben", 1.2), ("Cy", 4.0)], [("Cy", 0.8), ("Ben", 3.0)]),
                         ["Cy", "Ana", "Ben"])


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        self.assertTrue(sol.is_min_heap([1, 3, 2, 7, 4]))
        self.assertFalse(sol.is_min_heap([3, 1]))
        for n in (10, 100, 1000):
            self.assertLess(sol.heapify_swaps(list(range(n, 0, -1))), n)
        self.assertEqual(sol.heap_sort_with_heap([5, 1, 4, 1]), [1, 1, 4, 5])
        self.assertEqual(sol.kth_smallest_via_heapify([7, 2, 9, 4, 1], 3), 4)


if __name__ == "__main__":
    unittest.main()
