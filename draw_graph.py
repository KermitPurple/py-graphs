#!/usr/bin/env python3

from typing import Set, List
from graph import Graph
import pygame
import pygame_tools as pgt

class DisplayGraph(pgt.GameScreen, Graph):
    def __init__(self):
        Graph.__init__(self)
        pygame.init()
        size = pgt.Point(1300, 750)
        pgt.GameScreen.__init__(
            self,
            pygame.display.set_mode(size),
            size,
            (size.x // 2, size.y // 2)
        )

    @staticmethod
    def build(vertices: Set[str], edges: List[Set[str]]) -> 'DisplayGraph':
        '''
        builds a display graph from the given verticies and edges
        '''
        g = DisplayGraph()
        for vertex in vertices:
            g.add_vertex(vertex)
        for edge in edges:
            g.add_edge(*edge)
        return g

    def update(self):
        self.screen.fill((0, 0, 0))

def main():
    '''driver code'''
    g = DisplayGraph.build(
        {'a', 'b', 'c'},
        [
            {'a', 'b'},
            {'b', 'c'}
        ]
    )
    g.run()

if __name__ == "__main__":
    main()

