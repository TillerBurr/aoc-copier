from dataclasses import dataclass
from typing import Literal, Self


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def move(self, other_x: int, other_y: int) -> Self:
        return Point(self.x + other_x, self.y + other_y)

    def __add__(self, other: Self) -> Self:
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Self) -> Self:
        return Point(self.x - other.x, self.y - other.y)

    def adjacent_dist(self, other: Self) -> int:
        return max(abs(self.x - other.x), abs(self.y - other.y))

    def manhattan_distance(self, other: Self) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def dx(self, other: Self) -> int:
        return self.x - other.x

    def dy(self, other: Self) -> int:
        return self.y - other.y

    @property
    def coords(self) -> tuple[int, int]:
        return (self.x, self.y)

    def get_adjacent(self) -> tuple[Self, Self, Self, Self]:
        return (
            Point(self.x + 1, self.y),
            Point(self.x - 1, self.y),
            Point(self.x, self.y + 1),
            Point(self.x, self.y - 1),
        )


@dataclass
class Movement:
    direction: Literal["U"] | Literal["D"] | Literal["L"] | Literal["R"]
    amount: int


DIRECTIONS = {"U": Point(0, 1), "D": Point(0, -1), "L": Point(-1, 0), "R": Point(1, 0)}
