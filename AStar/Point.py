class Coord:
    x: int = 0
    y: int = 0

    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def equal(self, c):
        return self.x == c.x and self.y == c.y


class Point:
    coord: Coord = Coord(0, 0)

    parentID: int = -1

    priority: int = 0
    cost: int = 0

    def __init__(self, coord: Coord, cost: int = 0):
        self.coord = coord
        self.cost = cost

    def equal(self, p):
        return self.coord.equal(p.coord)

    def get_parent(self, point_set: list):
        return point_set[self.parentID]
