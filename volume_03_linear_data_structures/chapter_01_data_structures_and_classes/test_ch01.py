import random
import unittest

import ch01_examples as ex
import ch01_solutions as sol


class TestExamples(unittest.TestCase):
    def test_animal(self) -> None:
        leo, zara = ex.Animal("Leo", "lion"), ex.Animal("Zara", "zebra")
        leo.feed()
        self.assertEqual(leo.describe(), "Leo the lion has eaten 1 meal(s)")
        self.assertEqual(zara.meals_today, 0)            # objects keep separate data

    def test_book(self) -> None:
        self.assertEqual(ex.Book("Matilda", "Roald Dahl", 1988), ex.Book("Matilda", "Roald Dahl", 1988))

    def test_bank_invariant(self) -> None:
        account = ex.BankAccount("Maya", 100)
        account.deposit(50)
        account.withdraw(30)
        self.assertEqual(account.balance, 120)
        self.assertEqual(account.history(), ["+50", "-30"])
        for bad in (lambda: account.withdraw(1000), lambda: account.deposit(0),
                    lambda: account.withdraw(-5), lambda: ex.BankAccount("X", -1)):
            with self.assertRaises(ValueError):
                bad()
        self.assertEqual(account.balance, 120)
        account.history().append("hack")
        self.assertEqual(account.history(), ["+50", "-30"])
        with self.assertRaises(AttributeError):
            account.balance = 5  # type: ignore[misc]
        self.assertIn("balance=120", repr(account))

    def test_random_operations_keep_invariant(self) -> None:
        rng = random.Random(3)
        account = ex.BankAccount("R", 0)
        for _ in range(2000):
            try:
                if rng.random() < 0.5:
                    account.deposit(rng.randint(-5, 50))
                else:
                    account.withdraw(rng.randint(-5, 80))
            except ValueError:
                pass
            self.assertGreaterEqual(account.balance, 0)

    def test_bags_behave_the_same(self) -> None:
        rng = random.Random(1)
        fruits = [rng.choice(["apple", "kiwi", "mango", "fig"]) for _ in range(200)]
        a, b = ex.fill_bag(ex.ListBag(), fruits), ex.fill_bag(ex.CountingBag(), fruits)
        self.assertEqual(len(a), len(b))
        for fruit in ("apple", "kiwi", "mango", "fig", "pear"):
            self.assertEqual(a.count(fruit), b.count(fruit))
            self.assertEqual(fruit in a, fruit in b)
        self.assertEqual(sorted(a), sorted(b))


class TestSolutions(unittest.TestCase):
    def test_counter_rectangle(self) -> None:
        c = sol.Counter()
        for _ in range(5):
            c.click()
        self.assertEqual(c.value, 5)
        c.reset()
        self.assertEqual(c.value, 0)
        r = sol.Rectangle(8, 5)
        self.assertEqual((r.area(), r.perimeter()), (40, 26))

    def test_thermostat(self) -> None:
        self.assertEqual(sol.Thermostat(45).target, 30)
        t = sol.Thermostat()
        t.set_target(3)
        self.assertEqual(t.target, 10)
        t.set_target(22.5)
        self.assertEqual(t.target, 22.5)

    def test_playlist_and_parking(self) -> None:
        p = sol.Playlist("Trip")
        p.add("A")
        self.assertEqual(len(p), 1)
        self.assertIn("A", p)
        self.assertEqual(len(sol.Playlist("Other")), 0)    # default_factory gives each its own list
        lot = sol.ParkingLot(2)
        self.assertEqual([lot.park("KA01"), lot.park("KA01"), lot.park("KA02"), lot.park("KA03")],
                         [True, False, True, False])
        self.assertTrue(lot.leave("KA01"))
        self.assertFalse(lot.leave("KA01"))
        self.assertEqual(lot.free_spaces(), 1)


if __name__ == "__main__":
    unittest.main()
