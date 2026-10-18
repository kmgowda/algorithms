"""Chapter 1 - Solutions to the exercises."""

from __future__ import annotations


def brush_teeth_steps() -> list[str]:
    """Exercise 1: a precise, finite tooth-brushing algorithm."""
    return [
        "Pick up the toothbrush.",
        "Wet the bristles under the tap for 2 seconds.",
        "Squeeze a pea-sized amount of toothpaste onto the bristles.",
        "Brush the top teeth for 60 seconds.",
        "Brush the bottom teeth for 60 seconds.",
        "Spit out the toothpaste.",
        "Rinse the mouth with water once.",
        "Rinse the toothbrush and put it back.",
    ]


def is_precise(step: str) -> bool:
    """Exercise 3: flag vague words that make a step ambiguous."""
    vague_words = ("some", "a bit", "a little", "until it looks", "enough", "nicely", "maybe")
    lowered = step.lower()
    return not any(word in lowered for word in vague_words)


def traffic_light_action(color: str) -> str:
    """Exercise 4: what a driver does at a traffic light."""
    actions = {"green": "Go", "yellow": "Slow down and prepare to stop", "red": "Stop"}
    return actions.get(color.lower(), "Treat as a stop sign")


def elevator_direction(current_floor: int, requested_floor: int) -> str:
    """Exercise 5: which way should an elevator move?"""
    if requested_floor > current_floor:
        return "Up"
    if requested_floor < current_floor:
        return "Down"
    return "Open doors"


if __name__ == "__main__":
    for step in brush_teeth_steps():
        print(step, "-> precise" if is_precise(step) else "-> vague")
    print(traffic_light_action("Red"))
    print(elevator_direction(3, 7))
