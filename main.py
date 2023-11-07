import math

from AStar import AStar
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
    aStar.set_map(len(mapData[0]), len(mapData))
    aStar.update_map(lambda x, y: mapParser.map_parser(mapData, x, y))

    start, dest = mapParser.get_point(mapData)

    print("diag, manhattan")
    path = aStar.find(start, dest, True, True, aStar.get_manhattan_distance)
    mapParser.map_printer(mapData, path)

    print("diag, euclidean")
    path = aStar.find(start, dest, True, True,
                      lambda s, d: math.sqrt((s.x - d.x) ** 2 + (s.y - d.y) ** 2))
    mapParser.map_printer(mapData, path)

    print("normal, manhattan")
    path = aStar.find(start, dest, False, True, aStar.get_manhattan_distance)
    mapParser.map_printer(mapData, path)
