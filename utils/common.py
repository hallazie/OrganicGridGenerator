# coding:utf-8
# @author: xiao shanghua

from src.items import *

import math


def euc_distance(v1, v2):
    return math.sqrt((v1.x - v2.x) ** 2 + (v1.y - v2.y) ** 2)

