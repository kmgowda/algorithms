"""Volume 3, Chapter 1 - Solutions to the exercises."""

from __future__ import annotations

from dataclasses import dataclass, field


class Counter:
    """Exercise 1: a tally counter with click, reset, and value."""

    def __init__(self) -> None:
        self.value = 0

    def click(self) -> None:
        self.value += 1

    def reset(self) -> None:
        self.value = 0


@dataclass
class Rectangle:
    """Exercise 2: a garden plot."""
    width: float
    height: float

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


class Thermostat:
    """Exercise 3: invariant - the target temperature stays between 10 and 30 degrees."""
    LOW, HIGH = 10, 30

    def __init__(self, target: float = 20) -> None:
        self._target = 0.0
        self.set_target(target)

    @property
    def target(self) -> float:
        return self._target

    def set_target(self, value: float) -> None:
        self._target = min(max(value, self.LOW), self.HIGH)     # clamp into range


@dataclass
class Playlist:
    """Exercise 4: a playlist with __len__ and __contains__."""
    name: str
    songs: list[str] = field(default_factory=list)

    def add(self, song: str) -> None:
        self.songs.append(song)

    def __len__(self) -> int:
        return len(self.songs)

    def __contains__(self, song: str) -> bool:
        return song in self.songs


class ParkingLot:
    """Exercise 5: invariant - parked cars never exceed capacity, and no car is parked twice."""

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self._cars: set[str] = set()

    def park(self, plate: str) -> bool:
        if plate in self._cars or len(self._cars) >= self.capacity:
            return False
        self._cars.add(plate)
        return True

    def leave(self, plate: str) -> bool:
        if plate not in self._cars:
            return False
        self._cars.remove(plate)
        return True

    def free_spaces(self) -> int:
        return self.capacity - len(self._cars)


if __name__ == "__main__":
    c = Counter()
    c.click()
    print(c.value, Rectangle(8, 5).area(), Thermostat(45).target)
    p = Playlist("Road trip")
    p.add("Song A")
    print(len(p), "Song A" in p)
    lot = ParkingLot(2)
    print(lot.park("KA01"), lot.park("KA01"), lot.park("KA02"), lot.park("KA03"), lot.free_spaces())
