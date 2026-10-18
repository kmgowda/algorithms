"""Chapter 7 - Lists: Keeping Many Things in Order.

Run:  python3 ch07_examples.py
"""

from __future__ import annotations


def fruit_basket_demo() -> dict[str, object]:
    """Beginner example: the basic list operations on a fruit basket."""
    basket = ["apple", "banana", "cherry"]
    first = basket[0]                 # "apple"  - positions start at 0
    last = basket[-1]                 # "cherry" - negative positions count from the end
    basket.append("mango")            # add to the end
    basket.insert(1, "kiwi")          # add at position 1, shifting the rest right
    basket.remove("banana")           # remove the first "banana"
    popped = basket.pop()             # remove and return the last item ("mango")
    has_kiwi = "kiwi" in basket       # membership test
    return {"first": first, "last": last, "basket": basket, "popped": popped,
            "has_kiwi": has_kiwi, "size": len(basket)}


def attendance_report(class_list: list[str], present: list[str]) -> list[str]:
    """Practical example: who is absent today?"""
    absent = []
    for student in class_list:
        if student not in present:
            absent.append(student)
    return absent


def stops_between(route: list[str], start: str, end: str) -> list[str]:
    """Practical example: a bus route as a list. Slicing gives the stops you will pass."""
    i = route.index(start)
    j = route.index(end)
    if i <= j:
        return route[i:j + 1]
    return route[j:i + 1][::-1]       # travelling the other direction: reverse the slice


def feeding_grid() -> list[list[str]]:
    """Practical example: a list of lists - rows are days, columns are meal times."""
    return [
        ["fish", "fish", "squid"],      # Monday:    morning, noon, evening
        ["fish", "krill", "fish"],      # Tuesday
        ["squid", "fish", "fish"],      # Wednesday
    ]


def count_meals(grid: list[list[str]], food: str) -> int:
    """Walk every row and every column of a grid with nested loops."""
    count = 0
    for row in grid:
        for meal in row:
            if meal == food:
                count += 1
    return count


def playlist_after_actions(playlist: list[str], actions: list[tuple[str, str]]) -> list[str]:
    """Industry example: a music app updating a playlist.

    Each action is ("add", song), ("remove", song), ("play_next", song) or ("skip", "").
    """
    songs = list(playlist)            # make a copy so the caller's list is not changed
    for action, song in actions:
        if action == "add":
            songs.append(song)
        elif action == "play_next":
            songs.insert(0, song)
        elif action == "remove" and song in songs:
            songs.remove(song)
        elif action == "skip" and songs:
            songs.pop(0)
    return songs


def departures_board(flights: list[tuple[str, str, int]], now: int) -> list[str]:
    """Industry example: an airport board shows flights that have not left yet, by time.

    Each flight is (flight_code, city, departure_time_as_hhmm).
    """
    upcoming = [flight for flight in flights if flight[2] >= now]
    upcoming.sort(key=lambda flight: flight[2])
    return [f"{time:04d} {code} to {city}" for code, city, time in upcoming]


def aliasing_demo() -> tuple[list[str], list[str], list[str]]:
    """Two names for ONE list vs. a real copy."""
    original = ["lion", "tiger"]
    alias = original                  # same list, second name
    copy = original.copy()            # a brand-new list with the same items
    alias.append("bear")
    return original, alias, copy


def squares_up_to(n: int) -> list[int]:
    """A list comprehension: build a list in one line."""
    return [x * x for x in range(1, n + 1)]


if __name__ == "__main__":
    print(fruit_basket_demo())
    print("Absent:", attendance_report(["Ana", "Ben", "Cy", "Dev"], ["Ben", "Dev"]))
    route = ["Depot", "Library", "Market", "Hospital", "School"]
    print("Stops:", stops_between(route, "Library", "Hospital"))
    print("Fish meals:", count_meals(feeding_grid(), "fish"))
    print(playlist_after_actions(["Song A", "Song B"], [("add", "Song C"), ("play_next", "Song Z"), ("skip", "")]))
    print(departures_board([("AI202", "Delhi", 1430), ("BA118", "London", 915), ("EK501", "Dubai", 1105)], 1000))
    print(aliasing_demo())
    print(squares_up_to(5))
