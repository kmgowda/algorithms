import random
import unittest

import ch22_examples as ex


class TestChapter22(unittest.TestCase):
    def test_against_python_list(self) -> None:
        rng = random.Random(1)
        for _ in range(200):
            ref = [rng.randint(0, 9) for _ in range(rng.randint(0, 8))]
            ll = ex.LinkedList(ref)
            for _ in range(15):
                op, v = rng.choice(["front", "after", "delete"]), rng.randint(0, 9)
                if op == "front":
                    ll.push_front(v)
                    ref.insert(0, v)
                elif op == "after" and ref:
                    target = rng.choice(ref)
                    ll.insert_after(ll.find(target), v)
                    ref.insert(ref.index(target) + 1, v)
                elif op == "delete":
                    self.assertEqual(ll.delete(v), v in ref)
                    if v in ref:
                        ref.remove(v)
                self.assertEqual(ll.values(), ref)

    def test_waiting_list(self) -> None:
        rng = random.Random(2)
        for _ in range(200):
            w, ref, k = ex.WaitingList(), [], 0
            for _ in range(20):
                op = rng.choice(["join", "join", "cancel", "serve"])
                if op == "join":
                    w.join(f"r{k}")
                    ref.append(f"r{k}")
                    k += 1
                elif op == "cancel" and ref:
                    name = rng.choice(ref)
                    w.cancel(name)
                    ref.remove(name)
                elif op == "serve" and ref:
                    self.assertEqual(w.serve(), ref.pop(0))
                self.assertEqual(w.names(), ref)


if __name__ == "__main__":
    unittest.main()
