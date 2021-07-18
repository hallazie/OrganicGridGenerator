# coding:utf-8
# @author: xiao shanghua

from src.items import *

import math


class HexagonGrow:
    def __init__(self):
        pass

    @staticmethod
    def generate(**kwargs):

        layer = kwargs.get('layer', 5)
        long_edge_size = kwargs.get('long_edge_size', 2)

        root3 = math.sqrt(3)
        offset_list = [
            (0, 2),
            (root3, 1),
            (root3, -1),
            (0, -2),
            (-root3, -1),
            (-root3, 1)
        ]

        def traverse(queue: list, vlist: list, gsize: int):
            if not queue:
                return
            origin = queue.pop(0)
            if origin.layer >= gsize:
                return
            for offset in offset_list:
                vertex = Vertex(origin.x + offset[0], origin.y + offset[1], origin.layer+1)
                if vertex in vlist:
                    continue
                queue.append(vertex)
                vlist.append(vertex)
            traverse(queue, vlist, gsize)

        vertex_queue, vertex_list = [Vertex(0, 0, 0)], [Vertex(0, 0)]
        traverse(vertex_queue, vertex_list, layer)
        return vertex_list


