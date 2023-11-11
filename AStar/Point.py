from typing import Self


class Coord:
    x: int = 0
    y: int = 0

    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.equal(other)

    def equal(self, c) -> bool:
        return self.x == c.x and self.y == c.y


class Point:
    coord: Coord = Coord(0, 0)

    parentID: int = -1

    priority: int = 0
    cost: int = 0

    def __init__(self, coord: Coord, cost: int = 0):
        self.coord = coord
        self.cost = cost

    def __eq__(self, other):
        return self.equal(other)

    def equal(self, p) -> bool:
        return self.coord.equal(p.coord)

    # Return self type
    # https://stackoverflow.com/questions/33533148/how-do-i-type-hint-a-method-with-the-type-of-the-enclosing-class
    def get_parent(self, point_set: list[Self]) -> Self:
        return point_set[self.parentID]
