# coding:utf-8
# @author: xiao shanghua

from scipy.spatial import Delaunay
from src.items import *

import numpy as np


class GridGeneration:
    def __init__(self):
        pass

    @staticmethod
    def _gen_delaunay(vertex_list):
        point_list = np.array([(x.x, x.y) for x in vertex_list])
        triangular = Delaunay(point_list)
        vertex_list = [Vertex(x[0], x[1]) for x in triangular.points]
        poly_list = [Polygon([vertex_list[x[0]], vertex_list[x[1]], vertex_list[x[2]]]) for x in triangular.simplices]
        
        return poly_list

    def generate(self, vertex_list, method='delaunay'):
        """
        :param vertex_list
        :param method:
        :return:
        """
        if method == 'delaunay':
            return self._gen_delaunay(vertex_list)
        else:
            raise ValueError(f'generate grid {method} not supported (hexagon / binomial / gaussian / poisson)')



