# coding:utf-8
# @author: xiao shanghua

from src.items import *

import math


class VertexGeneration:
    def __init__(self):
        pass

    def _gen_binomial(self, **kw_args):
        raise NotImplemented

    def _gen_gaussian(self, **kw_args):
        raise NotImplemented

    def _gen_poisson(self, **kw_args):
        raise NotImplemented

    @staticmethod
    def _gen_hexagon(**kw_args):

        layer = 5
        if 'layer' in kw_args:
            layer = kw_args['layer']

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

    def generate(self, method='hexagon', **args):
        """
        :param method:
            * hexagon - evenly hexagon
            * binomial - binomial sampled
            * gaussian - gaussian sampled
            * poisson - poisson disk sampled [https://www.cct.lsu.edu/~fharhad/ganbatte/siggraph2007/CD2/content/sketches/0250.pdf]
        :return: list of vertex
        """
        if method == 'hexagon':
            return self._gen_hexagon(**args)
        elif method == 'binomial':
            return self._gen_binomial(**args)
        elif method == 'gaussian':
            return self._gen_gaussian(**args)
        elif method == 'poisson':
            return self._gen_poisson(**args)
        else:
            raise ValueError(f'generate vertex {method} not supported (hexagon / binomial / gaussian / poisson)')

    def random_jitter(self, vertex_list, jitter=0.1):
        pass

