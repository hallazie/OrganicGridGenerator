# coding:utf-8
# @author: xiao shanghua

import functools


class Vertex:
    def __init__(self, x, y, layer=None):
        self.x = x
        self.y = y
        self.layer = layer

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'x={self.x}, y={self.y}'

    def __hash__(self):
        return hash(self.__repr__())


class Polygon:
    """
    polygon, including tria, quad, etc.
    typ_: enumerate of:
        TRI for triang
        QUAD for quad
        OTHER for others
    """
    def __init__(self, vertex_list, typ_='TRI'):
        self.vertex_list = vertex_list
        self.type = typ_
        self._center = None
        self.sort_vertex_clockwise()

    @property
    def center(self):
        return self._center

    @center.getter
    def center(self):
        if self._center is None:
            center_x = sum([v.x for v in self.vertex_list]) / float(len(self.vertex_list))
            center_y = sum([v.y for v in self.vertex_list]) / float(len(self.vertex_list))
            self._center = Vertex(center_x, center_y)
        return self._center

    @center.setter
    def center(self, val):
        if type(val) is Vertex:
            self._center = val

    def _clockwise_dist(self, x, y):
        return (x.x - self.center.x) * (y.y - self.center.y) - (y.x - self.center.x) * (x.y - self.center.y)

    def _clockwise_comaprison(self, x: Vertex, y: Vertex):
        if x.x - self.center.x >= 0 and y.x - self.center.x < 0:
            return True
        if x.x - self.center.x < 0 and y.x - self.center.x >= 0:
            return False
        if x.x - self.center.x == 0 and y.x - self.center.x == 0:
            if x.y - self.center.y >= 0 or y.y - self.center.y >= 0:
                return x.y > y.y
            return y.y > x.y
        det = (x.x - self.center.x) * (y.y - self.center.y) - (y.x - self.center.x) * (x.y - self.center.y)
        if det < 0:
            return True
        elif det > 0:
            return False
        d1 = (x.x - self.center.x) * (x.x - self.center.x) + (x.y - self.center.y) * (x.y - self.center.y)
        d2 = (y.x - self.center.x) * (y.x - self.center.x) + (y.y - self.center.y) * (y.y - self.center.y)
        return d1 > d2

    def sort_vertex_clockwise(self):
        self.vertex_list = sorted(self.vertex_list, key=functools.cmp_to_key(lambda x, y: 1 if self._clockwise_comaprison(x, y) else -1))

    @staticmethod
    def find_plub(outlier, vertex1, vertex2):
        if abs(vertex1.x - vertex2.x) < 1e-5:
            return Vertex(vertex1.x, outlier.y)
        a = (vertex1.y - vertex2.y) / float(vertex1.x - vertex2.x)
        b = vertex1.y - a * vertex1.x
        m = outlier.x + a * outlier.y
        x = (m - a * b) / (a**2 + 1)
        y = (a * x + b)
        plub = Vertex(x, y)
        if plub == outlier or plub == vertex1 or plub == vertex2:
            print(f'false plub: {plub}, with x1={vertex1}, x2={vertex2}, y={outlier}')
        return plub

    @staticmethod
    def find_center(vertex1, vertex2):
        x = (vertex1.x + vertex2.x) / 2.
        y = (vertex1.y + vertex2.y) / 2.
        return Vertex(x, y)

    def split_to_quad(self):
        vertex_list = [self.vertex_list[-1]] + [v for v in self.vertex_list] + [self.vertex_list[0]]
        split_list = []
        for i in range(len(self.vertex_list)):
            v0, v1, v2 = vertex_list[i], vertex_list[i+1], vertex_list[i+2]
            c1 = self.find_center(v0, v1)
            c2 = self.find_center(v1, v2)
            poly = Polygon([c1, c2, v1, self.center])
            split_list.append(poly)
        # print(f'split to {len(split_list)} quads...')
        return split_list







