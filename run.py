# coding:utf-8
# @author: xiao shanghua

from src.items import *
from src.vertex_generator import VertexGeneration
from src.grid_generator import GridGeneration
from src.grid_modifier import GridModifier

import matplotlib.pyplot as plt
import numpy as np


def plot_polygon_grid(polygon_list_, vertex_list_):
    point_list = np.array([(x.x, x.y) for x in vertex_list_])
    for idx, poly in enumerate(polygon_list_):
        vert = [x for x in poly.vertex_list]
        vert.append(poly.vertex_list[0])
        for i in range(len(vert)-1):
            plt.plot([vert[i].x, vert[i+1].x], [vert[i].y, vert[i+1].y])
            # plt.arrow(vert[i].x, vert[i].y, vert[i+1].x-vert[i].x, vert[i+1].y-vert[i].y, head_width=0.05, head_length=0.1, fc='k', ec='k')
    plt.plot(point_list[:, 0], point_list[:, 1], 'o')
    plt.show()


if __name__ == '__main__':
    vg, gg, gm = VertexGeneration(), GridGeneration(), GridModifier()
    vertex_list = vg.generate('hexagon', layer=3)
    polygon_list = gg.generate(vertex_list)
    polygon_list = gm.random_merge(polygon_list, 0.33)
    polygon_list = gm.split_to_quads(polygon_list)
    plot_polygon_grid(polygon_list, vertex_list)

