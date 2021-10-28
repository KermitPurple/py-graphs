#!/usr/bin/env python3

from typing import Set, List, Dict
from graph import Graph
import math
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
            pgt.Point(size.x // 2, size.y // 2)
        )
        self.center = pgt.Point(
            self.window_size.x // 2,
            self.window_size.y // 2
        )
        self.vertex_positions_radii =pgt.Point(
            self.center.x - 40,
            self.center.y - 40
        )
        self.vertex_positions = {}
        self.font = pygame.font.Font(pygame.font.get_default_font(), 18)

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
        g.vertex_positions = g.calculate_vertex_positions()
        return g

    def calculate_vertex_positions(self) -> Dict[str, pgt.Point]:
        '''
        get the positions for each vertex
        :returns: a dict of vertices and points
        '''
        size = len(self.vertices)
        if size == 0:
            return {}
        elif size == 1:
            return {list(self.vertices)[0]: pgt.Point(self.window_size.x // 2, self.window_size.y // 2)}
        result = {}
        for i, vertex in enumerate(self.vertices):
            rads = i / size * math.pi * 2
            result[vertex] = pgt.Point(
                math.cos(rads) * self.vertex_positions_radii.x + self.center.x,
                math.sin(rads) * self.vertex_positions_radii.y + self.center.y
            )
        return result

    def draw_vertices(self):
        '''Draw the verticies of the graph'''
        for vertex, position in self.vertex_positions.items():
            pygame.draw.circle(
                self.screen,
                (255, 255, 255),
                position,
                5
            )
            pygame.draw.circle(
                self.screen,
                (200, 200, 200),
                position,
                5,
                1
            )
            self.screen.blit(self.font.render(
                vertex,
                True,
                (150, 150, 150)
            ), position)

    def draw_edges(self):
        '''Draw the edges of the graph'''
        for v1, v2 in self.edges:
            pygame.draw.line(
                self.screen,
                (255, 255, 255),
                self.vertex_positions[v1],
                self.vertex_positions[v2],
                3
            )

    def update(self):
        self.screen.fill((0, 0, 0))
        self.draw_edges()
        self.draw_vertices()

def main():
    '''driver code'''
    g = DisplayGraph.build(
        {'a', 'b', 'c', 'd', 'e'},
        [
            {'a', 'b'},
            {'b', 'c'},
            {'a', 'c'},
            {'c', 'd'},
            {'a', 'd'},
            {'b', 'e'}
        ]
    )
    g.run()

if __name__ == "__main__":
    main()

