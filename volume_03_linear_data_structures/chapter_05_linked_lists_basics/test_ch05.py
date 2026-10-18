import random
import unittest

import ch05_examples as ex
import ch05_solutions as sol
from ch05_examples import LinkedList


def check_invariants(test: unittest.TestCase, lst: LinkedList) -> None:
    count, node, last = 0, lst._head, None
    while node is not None:
        count, last, node = count + 1, node, node.next
    test.assertEqual(count, len(lst))
    test.assertIs(lst._tail, last)


class TestLinkedList(unittest.TestCase):
    def test_basics(self) -> None:
        lst = LinkedList(["Depot", "Library"])
        lst.append("School")
        lst.push_front("Garage")
        self.assertEqual(list(lst), ["Garage", "Depot", "Library", "School"])
        self.assertEqual(lst[2], "Library")
        self.assertEqual(lst.find("School"), 3)
        self.assertEqual(lst.find("Zoo"), -1)
        self.assertEqual(repr(LinkedList()), "None")
        self.assertEqual(repr(LinkedList([1])), "1 -> None")
        with self.assertRaises(IndexError):
            LinkedList().pop_front()
        with self.assertRaises(IndexError):
            lst[10]
        check_invariants(self, lst)

    def test_against_model(self) -> None:
        rng = random.Random(5)
        lst, model = LinkedList(), []
        for _ in range(3000):
            op = rng.random()
            if op < 0.25:
                v = rng.randint(0, 9)
                lst.append(v)
                model.append(v)
            elif op < 0.45:
                v = rng.randint(0, 9)
                lst.push_front(v)
                model.insert(0, v)
            elif op < 0.6 and model:
                self.assertEqual(lst.pop_front(), model.pop(0))
            elif op < 0.75 and model:
                i = rng.randrange(len(model))
                v = rng.randint(0, 9)
                lst.insert_after(i, v)
                model.insert(i + 1, v)
            elif op < 0.9:
                v = rng.randint(0, 9)
                self.assertEqual(lst.remove(v), v in model)
                if v in model:
                    model.remove(v)
            else:
                lst.reverse()
                model.reverse()
            self.assertEqual(list(lst), model)
            check_invariants(self, lst)

    def test_examples(self) -> None:
        self.assertEqual(ex.treasure_hunt(["a", "b"]), ["step 1: a", "step 2: b"])
        self.assertEqual(ex.train_after_coupling(["Car 1", "Car 2", "Car 3"], "Engine", "Car 2"),
                         ["Engine", "Car 1", "Car 2", "Dining car", "Car 3"])
        self.assertEqual(ex.browser_tabs_closed(["Mail", "News", "Maps", "Music"], ["News", "Music"]),
                         ["Mail", "Maps"])


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        self.assertEqual(sol.count_nodes_recursive(sol.build([3, 1, 4])), 3)
        self.assertEqual(sol.count_nodes_recursive(None), 0)
        self.assertEqual(sol.sum_values(sol.build([3, 1, 4])), 8)
        for values in ([], [1], [1, 2, 3, 4]):
            self.assertEqual(sol.to_list(sol.reverse_chain(sol.build(values))), values[::-1])
        rng = random.Random(9)
        for _ in range(200):
            a = sorted(rng.randint(0, 20) for _ in range(rng.randint(0, 8)))
            b = sorted(rng.randint(0, 20) for _ in range(rng.randint(0, 8)))
            self.assertEqual(sol.to_list(sol.merge_sorted(sol.build(a), sol.build(b))), sorted(a + b))
            c = sorted(a + b)
            self.assertEqual(sol.to_list(sol.remove_duplicates_sorted(sol.build(c))), sorted(set(c)))


if __name__ == "__main__":
    unittest.main()
