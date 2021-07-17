# coding:utf-8
# @author: xiao shanghua

from src.items import *
from src.vertex_generator import VertexGeneration
from src.grid_generator import GridGeneration
from src.grid_modifier import GridModifier
from src.grid_relaxation import GridRelaxation

import matplotlib.pyplot as plt
import matplotlib.animation as ani
import numpy as np
import random
import copy


def plot_polygon_grid(polygon_list_, vertex_list_=None):
    for idx, poly in enumerate(polygon_list_):
        vert = [x for x in poly.vertex_list]
        vert.append(poly.vertex_list[0])
        for i in range(len(vert)-1):
            plt.plot([vert[i].x, vert[i+1].x], [vert[i].y, vert[i+1].y])
            # plt.arrow(vert[i].x, vert[i].y, vert[i+1].x-vert[i].x, vert[i+1].y-vert[i].y, head_width=0.05, head_length=0.1, fc='k', ec='k')
    if not vertex_list_:
        vertex_list_ = set()
        for poly in polygon_list_:
            for vertex in poly.vertex_list:
                if vertex not in vertex_list_:
                    vertex_list_.add(vertex)
        vertex_list_ = list(vertex_list_)
    point_list = np.array([(x.x, x.y) for x in vertex_list_])
    plt.plot(point_list[:, 0], point_list[:, 1], 'o')


def randomize_polygon_vertex_by_jitter(p_list, jitter=0.1):
    for poly in p_list:
        for vertex in poly.vertex_list:
            jitter_x = random.randrange(-1, 1) * jitter
            jitter_y = random.randrange(-1, 1) * jitter
            vertex.x += jitter_x
            vertex.y += jitter_y


def plot_animation():
    vg, gg, gm, gr = VertexGeneration(), GridGeneration(), GridModifier(), GridRelaxation()
    fig, ax = plt.subplots()

    polygon_total = []

    vertex_list = vg.generate('hexagon', layer=3)
    polygon_list = gg.generate(vertex_list)
    polygon_list = gm.random_merge(polygon_list, 0.125)
    polygon_list = gm.split_to_quads(polygon_list)
    polygon_list = gm.unify_vertex(polygon_list)

    # polygon_list = [Polygon([Vertex(0, 0), Vertex(1.7, 0.7), Vertex(2, 2), Vertex(0.7, 1.7)])]

    for i in range(100):
        polygon_total.append(copy.deepcopy(polygon_list))
        polygon_list = gr.relaxation(polygon_list, epochs=1, learning_rate=0.025)

    def plot_animation_call(idx):
        ax.clear()
        for idx, poly in enumerate(polygon_total[idx % len(polygon_total)]):
            vert = [x for x in poly.vertex_list]
            vert.append(poly.vertex_list[0])
            for j in range(len(vert)-1):
                plt.plot([vert[j].x, vert[j+1].x], [vert[j].y, vert[j+1].y])

    animator = ani.FuncAnimation(fig, plot_animation_call, interval=20)
    # animator.save('output//grid-generation.gif')
    plt.show()


def plot_static():
    vg, gg, gm, gr = VertexGeneration(), GridGeneration(), GridModifier(), GridRelaxation()
    vertex_list = vg.generate('hexagon', layer=3)
    polygon_list = gg.generate(vertex_list)
    polygon_list = gm.random_merge(polygon_list, 0.125)
    polygon_list = gm.split_to_quads(polygon_list)
    polygon_list = gm.unify_vertex(polygon_list)
    polygon_list = gr.relaxation(polygon_list, epochs=70, learning_rate=0.05)
    # polygon_list = [Polygon([Vertex(0, 0), Vertex(1.7, 0.7), Vertex(2, 2), Vertex(0.7, 1.7)])]
    plot_polygon_grid(polygon_list)
    plt.show()


if __name__ == '__main__':
    plot_animation()



