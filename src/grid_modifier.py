# coding:utf-8
# @author: xiao shanghua

from src.items import *

import random


class GridModifier:
    def __init__(self):
        pass

    @staticmethod
    def split_to_quads(poly_list):
        """
        :param poly_list:
        :return:
        """
        quad_list = []
        for poly in poly_list:
            quad_list.extend(poly.split_to_quad())
        return quad_list

    @staticmethod
    def random_merge(poly_list, merge_thresh=0.5):
        """

        :param poly_list:
        :param merge_thresh:
        :return:
        """
        merg_list, siz1 = [], len(poly_list)
        while poly_list:
            head = poly_list.pop()
            subs = []
            if random.random() <= merge_thresh:
                merg_list.append(head)
                continue
            for other in poly_list:
                inter = len(set(other.vertex_list) & set(head.vertex_list))
                if inter != 2:
                    continue
                subs.append(other)
            if not subs:
                merg_list.append(head)
                continue
            random.shuffle(subs)
            tail = subs[0]
            poly_list.remove(tail)
            merg = Polygon(list(set(head.vertex_list) | set(tail.vertex_list)))
            merg_list.append(merg)
        siz2 = len(merg_list)
        print(f'merge vertex from size {siz1} -> {siz2}')
        return merg_list

    @staticmethod
    def relaxation(polygon_list):
        raise NotImplemented


