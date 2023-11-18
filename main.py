import math
from typing import Callable

from AStar import AStar, Point
from AStar.MapParser import MapParser

# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    mapData = [
        '##############################',
        '#         #              #   #',
        '# ####    ########       #   #',
        '#  O #    #              #   #',
        '#    ###     #####  ######   #',
        '#      #   ###   #           #',
        '#      #     #   #  #  #   ###',
        '#     #####    #    #  # X   #',
        '#              #       #     #',
        '##############################'
    ]

    mapParser = MapParser()

    aStar = AStar.AStar()
    if not aStar.set_map(len(mapData[0]), len(mapData)):
        print("invalid map data")
        exit(-1)

    aStar.update_map(lambda x, y: mapParser.map_parser(mapData, x, y))

    start, dest = mapParser.get_point(mapData)


    def path_finder(start_point: Point.Coord, dest_point: Point.Coord, diag: bool, check_corner: bool,
                    heuristic: Callable[[Point.Coord, Point.Coord], int | float]):
        bPathFound, path = aStar.find(start_point, dest_point, diag, check_corner, heuristic)
        if not bPathFound:
            print("path not found")
            return

        mapParser.map_printer(mapData, path)


    # ------------
    print("diag, manhattan")
    path_finder(start, dest, True, True, aStar.get_manhattan_distance)

    # ------------
    print("diag, euclidean")
    path_finder(start, dest, True, True,
                lambda s, d: math.sqrt((s.x - d.x) ** 2 + (s.y - d.y) ** 2))

    # ------------
    print("normal, manhattan")
    path_finder(start, dest, False, True, aStar.get_manhattan_distance)

    # ------------
    print("invalid path")
    path_finder(start, Point.Coord(65535, 65535), False, True, aStar.get_manhattan_distance)
