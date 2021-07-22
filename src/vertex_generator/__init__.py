# coding:utf-8
# @author: xiao shanghua

from src.items import *
from src.vertex_generator.hexagon import HexagonGrow
from src.vertex_generator.poisson_disc import PoissonDiscSample
from src.vertex_generator.orthogonal import OrthogonalGridGenerator

import math
import sys

sys.setrecursionlimit(10**8)
print(f'system maximum recurse limit={sys.getrecursionlimit()}')


class VertexGeneration:
    def __init__(self):
        self.hexagon_sampler = None
        self.poisson_disc_sampler = None
        self.orthogonal_sampler = None

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
            if self.hexagon_sampler is None:
                self.hexagon_sampler = HexagonGrow()
            return self.hexagon_sampler.generate(**args)
        elif method == 'binomial':
            raise NotImplemented
        elif method == 'gaussian':
            raise NotImplemented
        elif method == 'poisson':
            if self.poisson_disc_sampler is None:
                self.poisson_disc_sampler = PoissonDiscSample()
            return self.poisson_disc_sampler.generate(**args)
        elif method == 'orthogonal':
            if self.orthogonal_sampler is None:
                self.orthogonal_sampler = OrthogonalGridGenerator()
            return self.orthogonal_sampler.generate(**args)
        else:
            raise ValueError(f'generate vertex {method} not supported (hexagon / binomial / gaussian / poisson)')

    def random_jitter(self, vertex_list, jitter=0.1):
        pass

