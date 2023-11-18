from operator import attrgetter
from typing import TypeVar, Callable

from AStar import Point


class AStar:
    bInit: bool = False

    width: int = 0
    height: int = 0

    path: int = 0
    obstacle: int = 255

    mapData: list[int] = []

    step_cost_normal: int = 10
    step_cost_diagonal: int = 14

    class Offset:
        x: int = 0
        y: int = 0
        cost: int = 0

        def __init__(self, x: int, y: int, cost: int):
            self.x = x
            self.y = y
            self.cost = cost

    normalNeighbour: list[Offset] = [
        Offset(1, 0, step_cost_normal),
        Offset(0, 1, step_cost_normal),
        Offset(-1, 0, step_cost_normal),
        Offset(0, -1, step_cost_normal),
    ]
    diagonalNeighbour: list[Offset] = [
        Offset(1, 0, step_cost_normal),
        Offset(1, 1, step_cost_diagonal),
        Offset(0, 1, step_cost_normal),
        Offset(-1, 1, step_cost_diagonal),
        Offset(-1, 0, step_cost_normal),
        Offset(-1, -1, step_cost_diagonal),
        Offset(0, -1, step_cost_normal),
        Offset(1, -1, step_cost_diagonal)
    ]

    def __init__(self):
        return

    def set_map(self, width: int, height: int) -> bool:
        def valid(sz: int) -> bool:
            if sz <= 0:
                return False
            return True

        self.bInit = False

        if not (valid(width) and valid(height)):
            return False

        self.width = width
        self.height = height

        for idx in range(self.width * self.height):
            self.mapData.append(self.path)

        self.bInit = True

        return True

    def get_map_offset(self, x: int, y: int) -> int:
        return y * self.width + x

    def offset_valid(self, offset: int) -> bool:
        return 0 <= offset < self.width * self.height

    def set_map_data(self, x: int, y: int, cost: int):
        offset = self.get_map_offset(x, y)

        if self.offset_valid(offset):
            self.mapData[offset] = cost

    def get_map_data(self, x: int, y: int) -> int:
        offset = self.get_map_offset(x, y)

        if self.offset_valid(offset):
            return self.mapData[offset]

        return self.obstacle

    def map_obstacle(self, x: int, y: int) -> int:
        return self.get_map_data(x, y) == self.obstacle

    # Callback type:
    # https://docs.python.org/zh-cn/3.10/library/typing.html#callable
    def iterate_map(self, cb: Callable[[int, int, int], None]):
        """
        callback: std::function<void(int x, int y, int cost)>
        """
        for y in range(self.height):
            for x in range(self.width):
                cb(x, y, self.get_map_data(x, y))

    def update_map(self, cb: Callable[[int, int], int]) -> bool:
        """
        callback: std::function<int(int x, int y)>
        """
        if not self.bInit:
            return False

        self.iterate_map(lambda x, y, cost: self.set_map_data(x, y, cb(x, y)))

        return True

    @staticmethod
    def get_manhattan_distance(start: Point.Coord, dest: Point.Coord) -> int:
        return abs(start.x - dest.x) + abs(start.y - dest.y)

    # Generic
    # https://docs.python.org/zh-cn/3.10/library/typing.html#callable
    T = TypeVar('T')

    @staticmethod
    def find_list(lst: list[T], item: T) -> int:
        index: int = -1
        for idx in range(len(lst)):
            # if lst[idx].equal(item):
            if lst[idx] == item:
                index = idx

        return index

    def find(self, start: Point.Coord, dest: Point.Coord, diag: bool, check_corner: bool,
             heuristic: Callable[[Point.Coord, Point.Coord], int | float]) \
            -> [bool, list[Point.Coord]]:
        """
        heuristic callback: std::function<int(Point::Coord start, Point::Coord dest)>
        """
        open_set: list[Point.Point] = []
        close_set: list[Point.Point] = []
        point_set: list[Point.Point] = []

        path: list[Point.Coord] = []

        if self.map_obstacle(start.x, start.y) or self.map_obstacle(dest.x, dest.y):
            return [False, path]

        open_set.append(Point.Point(start))
        neighbour = self.diagonalNeighbour if diag else self.normalNeighbour

        while len(open_set) != 0:
            # open_set.sort(key=lambda p: p.priority)
            open_set.sort(key=attrgetter('priority'), reverse=True)

            base = open_set[len(open_set) - 1]

            if base.coord.equal(dest):
                path.append(base.coord)
                parentIdx: int = base.parentID

                while parentIdx != -1:
                    parent = point_set[parentIdx]
                    path.append(parent.coord)
                    parentIdx = parent.parentID

                path.reverse()
                return [True, path]

            open_set.pop()
            close_set.append(base)

            for i in range(len(neighbour)):
                offsetX = neighbour[i].x
                offsetY = neighbour[i].y
                cost = neighbour[i].cost

                neighCoord: Point.Coord = Point.Coord(base.coord.x + offsetX, base.coord.y + offsetY)
                curCost: int = self.get_map_data(neighCoord.x, neighCoord.y)

                neighPoint: Point.Point = Point.Point(neighCoord, base.cost + curCost + cost)

                if curCost == self.obstacle:
                    continue

                if diag and check_corner and (i % 2 == 1):
                    prevIdx = i - 1
                    nextIdx = (i + 1) % len(neighbour)

                    if (self.map_obstacle(base.coord.x + neighbour[prevIdx].x,
                                          base.coord.y + neighbour[prevIdx].y)
                            and self.map_obstacle(base.coord.x + neighbour[nextIdx].x,
                                                  base.coord.y + neighbour[nextIdx].y)):
                        continue

                if self.find_list(close_set, neighPoint) != -1:
                    continue

                def update_point(cur: Point.Point):
                    cur.cost = neighPoint.cost
                    cur.priority = heuristic(neighPoint.coord, dest) + neighPoint.cost

                    index = self.find_list(point_set, base)

                    if index == -1:
                        point_set.append(base)
                        cur.parentID = len(point_set) - 1
                    else:
                        cur.parentID = index

                nextIdx = self.find_list(open_set, neighPoint)

                if nextIdx == -1:
                    update_point(neighPoint)
                    open_set.append(neighPoint)
                elif open_set[nextIdx].cost > neighPoint.cost:
                    update_point(open_set[nextIdx])

        return [False, path]
