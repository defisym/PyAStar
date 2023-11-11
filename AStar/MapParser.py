from AStar import AStar, Point


class MapParser:
    obstacle = '#'
    start = 'O'
    dest = 'X'
    path = '·'

    def __init__(self, obstacle='#', start='O', dest='X', path='·'):
        self.obstacle = obstacle
        self.start = start
        self.dest = dest
        self.path = path

    def map_parser(self, data: list[str], x: int, y: int) -> int:
        if y < 0 or y >= len(data):
            return AStar.AStar.obstacle

        if x < 0 or x >= len(data[y]):
            return AStar.AStar.obstacle

        curChar = data[y][x]

        if curChar == self.obstacle:
            return AStar.AStar.obstacle

        return AStar.AStar.path

    def get_point(self, data: list[str]) -> [Point.Coord, Point.Coord]:
        start_point = Point.Coord(0, 0)
        dest_point = Point.Coord(0, 0)

        for y in range(len(data)):
            for x in range(len(data[y])):
                curChar = data[y][x]

                if curChar == self.start:
                    start_point = Point.Coord(x, y)

                if curChar == self.dest:
                    dest_point = Point.Coord(x, y)

        return [start_point, dest_point]

    def map_printer(self, data: list[str], path: list[Point.Coord]):
        for y in range(len(data)):
            for x in range(len(data[y])):
                curChar = data[y][x]

                if ((not (curChar == self.start or curChar == self.dest))
                        and AStar.AStar.find_list(path, Point.Coord(x, y)) != -1):
                    curChar = self.path

                print(curChar, end='')

            # new line
            print()

        # new line
        print()
