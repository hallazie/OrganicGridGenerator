# --*-- coding:utf-8 --*--
# @author: xiao shanghua

from src.items import *

import random


class OrthogonalGridGenerator:
    def __init__(self):
        pass

    @staticmethod
    def get_poiint(x, y, jitter):
        x += random.random() * jitter
        y += random.random() * jitter
        return Vertex(x, y)

    def generate(self, **kwargs):
        vertex_list = []
        height = kwargs.get('height', 20)
        width = kwargs.get('width', 20)
        jitter = kwargs.get('jitter', 0.1)
        for i in range(width):
            for j in range(height):
                vertex_list.append(self.get_poiint(i, j, jitter))
        return vertex_list



