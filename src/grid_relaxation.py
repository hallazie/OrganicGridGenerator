# coding:utf-8
# @author: xiao shanghua

from src.items import *

import math


class GridRelaxation:
    def __init__(self):
        self.learning_rate = 0.1

    @staticmethod
    def _first_derivative(polygon: Polygon, alpha):
        """
        calc 1st derivative of D(a)
        :param polygon:
        :param alpha:
        :return:
        """
        if len(polygon.vertex_list) != 4:
            return
        radius = (polygon.side_length / 8.) * math.sqrt(2)
        v1, v2, v3, v4 = polygon.vertex_list
        derive = 2 * radius * math.sin(alpha * (v1.x - v2.y - v3.x + v4.y)) + 2 * radius * math.cos(alpha * (-v1.y - v2.x + v3.y + v4.x))
        return derive

    @staticmethod
    def _second_derive(polygon, alpha, radius):
        """
        calc 2ed derivative of D(a)
        :param polygon:
        :param alpha:
        :return:
        """
        if len(polygon.vertex_list) != 4:
            return 0.
        v1, v2, v3, v4 = polygon.vertex_list
        derive = 2 * radius * math.cos(alpha * (v1.x - v2.y - v3.x + v4.y)) + 2 * radius * math.sin(alpha * (v1.y + v2.x - v3.y - v4.x))
        return derive

    def _arg_min_alpha(self, polygon: Polygon, radius):
        if len(polygon.vertex_list) != 4:
            return 0.
        v1, v2, v3, v4 = polygon.vertex_list
        numerator = float(v1.y + v2.x - v3.y - v4.x)
        denominator = float(v1.x - v2.y + v3.x + v4.y)
        if denominator == 0:
            # already orthogonal, directly return 0
            return 0.
        const = math.atan(numerator / denominator)
        alpha1, alpha2 = const + math.pi, const - math.pi
        second_derive = self._second_derive(polygon, alpha1, radius)
        if second_derive < 0:
            return alpha1
        else:
            return alpha2

    @staticmethod
    def _corner_coords(center: Vertex, alpha, radius):
        sina, cosa = math.sin(alpha), math.cos(alpha)
        v1 = Vertex(center.x + radius * cosa, center.y + radius * sina)
        v2 = Vertex(center.x + radius * sina, center.y - radius * cosa)
        v3 = Vertex(center.x - radius * cosa, center.y - radius * sina)
        v4 = Vertex(center.x - radius * sina, center.y + radius * cosa)
        return v1, v2, v3, v4

    @staticmethod
    def _align_to_vertex(poly, square_list):
        closest = {}
        for vertex in poly.vertex_list:
            closest[vertex] = sorted(square_list, key=lambda x: euc_distance(x, vertex))[0]
        if len(set(closest.values())) == 4:
            return [closest[x] for x in poly.vertex_list]
        else:
            return poly.vertex_list

    def relax_single_step_update(self, polygon_list):
        differentiat = {}
        for poly in polygon_list:
            for vertex in poly.vertex_list:
                differentiat[id(vertex)] = {'x': [], 'y': []}
        for poly in polygon_list:
            center = poly.center
            # radius = (poly.side_length / 8.) * math.sqrt(2)
            radius = sorted([euc_distance(center, v) for v in poly.vertex_list])[0] * 0.8
            alpha = self._arg_min_alpha(poly, radius)
            v1, v2, v3, v4 = self._corner_coords(center, alpha, radius)
            align_list = self._align_to_vertex(poly, [v1, v2, v3, v4])
            v1, v2, v3, v4 = align_list
            # TODO fix p1->v1, p2->v2, etc. mapping
            differentiat[id(poly.vertex_list[0])]['x'].append((v1.x - poly.vertex_list[0].x) * self.learning_rate)
            differentiat[id(poly.vertex_list[0])]['y'].append((v1.y - poly.vertex_list[0].y) * self.learning_rate)
            differentiat[id(poly.vertex_list[1])]['x'].append((v2.x - poly.vertex_list[1].x) * self.learning_rate)
            differentiat[id(poly.vertex_list[1])]['y'].append((v2.y - poly.vertex_list[1].y) * self.learning_rate)
            differentiat[id(poly.vertex_list[2])]['x'].append((v3.x - poly.vertex_list[2].x) * self.learning_rate)
            differentiat[id(poly.vertex_list[2])]['y'].append((v3.y - poly.vertex_list[2].y) * self.learning_rate)
            differentiat[id(poly.vertex_list[3])]['x'].append((v4.x - poly.vertex_list[3].x) * self.learning_rate)
            differentiat[id(poly.vertex_list[3])]['y'].append((v4.y - poly.vertex_list[3].y) * self.learning_rate)
        for idx in differentiat:
            differentiat[idx]['x'] = (sum(differentiat[idx]['x']) / len(differentiat[idx]['x'])) if differentiat[idx]['x'] else 0
            differentiat[idx]['y'] = (sum(differentiat[idx]['y']) / len(differentiat[idx]['y'])) if differentiat[idx]['y'] else 0
        for poly in polygon_list:
            for vertex in poly.vertex_list:
                vertex.x += differentiat[id(vertex)]['x']
                vertex.y += differentiat[id(vertex)]['y']
            poly.recalc_center()

    def relax_single_polygon_by_step(self, polygon: Polygon):
        if len(polygon.vertex_list) != 4:
            # only used for quad relaxation
            return polygon
        center = polygon.center
        radius = (polygon.side_length / 8.) * math.sqrt(2)
        alpha = self._arg_min_alpha(polygon, radius)
        v1, v2, v3, v4 = self._corner_coords(center, alpha, radius)
        polygon.vertex_list[0].x = polygon.vertex_list[0].x + (v1.x - polygon.vertex_list[0].x) * self.learning_rate
        polygon.vertex_list[0].y = polygon.vertex_list[0].y + (v1.y - polygon.vertex_list[0].y) * self.learning_rate
        polygon.vertex_list[1].x = polygon.vertex_list[1].x + (v2.x - polygon.vertex_list[1].x) * self.learning_rate
        polygon.vertex_list[1].y = polygon.vertex_list[1].y + (v2.y - polygon.vertex_list[1].y) * self.learning_rate
        polygon.vertex_list[2].x = polygon.vertex_list[2].x + (v3.x - polygon.vertex_list[2].x) * self.learning_rate
        polygon.vertex_list[2].y = polygon.vertex_list[2].y + (v3.y - polygon.vertex_list[2].y) * self.learning_rate
        polygon.vertex_list[3].x = polygon.vertex_list[3].x + (v4.x - polygon.vertex_list[3].x) * self.learning_rate
        polygon.vertex_list[3].y = polygon.vertex_list[3].y + (v4.y - polygon.vertex_list[3].y) * self.learning_rate

    def relaxation(self, polygon_list, epochs=10, learning_rate=None):
        if learning_rate:
            self.learning_rate = learning_rate
        for ep in range(epochs):
            # for idx in range(len(polygon_list)):
            #     self.relax_single_polygon_by_step(polygon_list[idx])
            self.relax_single_step_update(polygon_list)
        return polygon_list


