#!/usr/bin/env python3

from typing import Set, List, Dict
from graph import Graph
import math
import pygame
import pygame_tools as pgt

class DisplayGraph(pgt.GameScreen, Graph):
    point_radius = 5
    possible_names = 'abcdefghijklmnopqrstuvwxyzABCDEFGJIJKLMNOPQRSTUVWXYZ'
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
        self.selected_vertex = None
        self.highlighted_vertex = None
        self.selected_edge = None
        self.adding_edge = False
        input_height = self.window_size.y // 4
        self.input_box = pgt.InputBox(
            pygame.Rect(
                self.window_size.x // 10,
                self.center.y - input_height // 2,
                self.window_size.x * 8 // 10,
                input_height,
            ),
            'darkgrey',
            'black',
            0,
            None,
            pygame.font.Font(pygame.font.get_default_font(), 40),
            True
        )
        self.getting_new_name = False

    def reset_input(self):
        self.input_box.reset()
        self.getting_new_name = False

    @classmethod
    def build(cls, vertices: Set[str], edges: List[Set[str]]) -> 'DisplayGraph':
        '''
        builds a display graph from the given vertices and edges
        '''
        g = super().build(vertices, edges)
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
        vertices = sorted(self.vertices)
        for i, vertex in enumerate(vertices):
            rads = i / size * math.pi * 2 - math.pi / 2
            result[vertex] = pgt.Point(
                math.cos(rads) * self.vertex_positions_radii.x + self.center.x,
                math.sin(rads) * self.vertex_positions_radii.y + self.center.y
            )
        return result

    def draw_vertices(self):
        '''Draw the vertices of the graph'''
        for vertex, position in self.vertex_positions.items():
            pygame.draw.circle(
                self.screen,
                (0, 255, 0 ) if vertex == self.highlighted_vertex else (255, 255, 255),
                position,
                self.point_radius
            )
            pygame.draw.circle(
                self.screen,
                (200, 200, 200),
                position,
                self.point_radius,
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
                (0, 255, 0) if self.selected_edge == {v1, v2} else (255, 255, 255),
                self.vertex_positions[v1],
                self.vertex_positions[v2],
                3
            )

    def draw_new_edge(self):
        '''draw a preview of a new edge'''
        if self.highlighted_vertex is None:
            return
        pygame.draw.line(
            self.screen,
            (0, 255, 0),
            self.vertex_positions[self.highlighted_vertex],
            self.get_scaled_mouse_pos(),
            3
        )

    def update_selected_vertex(self):
        '''move the selected vertex to the mouse position'''
        if self.selected_vertex is not None:
            self.vertex_positions[self.selected_vertex] = self.get_scaled_mouse_pos()

    def update(self):
        self.screen.fill((0, 0, 0))
        self.update_selected_vertex()
        self.draw_edges()
        self.draw_vertices()
        if self.adding_edge:
            self.draw_new_edge()
        if self.getting_new_name:
            self.input_box.draw(self.screen)

    def key_down(self, event: pygame.event.Event):
        '''
        called when key is pressed
        :event: event of when the key is pressed
        '''
        if self.getting_new_name:
            self.input_box.update(event)
            if self.input_box.done:
                self.rename_vertex(
                    self.highlighted_vertex,
                    self.input_box.get_value()
                )
                self.reset_input()
            return
        match event.unicode.lower():
            case 'r':
                self.vertex_positions = self.calculate_vertex_positions()
            case 'd' | '\x08':
                if self.highlighted_vertex is not None:
                    self.remove_vertex(self.highlighted_vertex)
                    self.highlighted_vertex = None
                elif self.selected_edge is not None:
                    self.remove_edge(*self.selected_edge)
                    self.selected_edge = None
            case 'a':
                vertex = self.add_new_vertex()
                if self.adding_edge:
                    self.adding_edge = False
                    self.add_edge(self.highlighted_vertex, vertex)
                self.selected_edge = None
                self.highlighted_vertex = None
            case 'e' if self.highlighted_vertex is not None:
                self.adding_edge = True
            case 'c':
                self.clear()
            case 'n' if self.highlighted_vertex is not None:
                self.getting_new_name = True

    def mouse_button_down(self, event: pygame.event.Event):
        '''
        called when mouse button is pressed
        :event: event of when the mouse button is pressed
        '''
        if event.button != 1: # not left click
            return
        self.reset_input()
        mouse_pos = self.get_scaled_mouse_pos()
        for vertex, pos in self.vertex_positions.items():
            if pgt.Point.distance(pos, mouse_pos) < self.point_radius:
                if self.adding_edge:
                    self.add_edge(self.highlighted_vertex, vertex)
                    self.adding_edge = False
                self.selected_vertex = vertex
                self.highlighted_vertex = vertex
                self.selected_edge = None
                return
        self.highlighted_vertex = None
        for v1, v2 in self.edges:
            d = pgt.Point.distance_from_line(
                self.vertex_positions[v1],
                self.vertex_positions[v2],
                mouse_pos
            )
            if d < 2:
                self.selected_edge = {v1, v2}
                return
        self.selected_edge = None

    def mouse_button_up(self, event: pygame.event.Event):
        '''
        called when mouse button is released
        :event: event of when the mouse button is released
        '''
        if event.button != 1: # not left click
            return
        self.selected_vertex = None

    def remove_vertex(self, vertex: str) -> bool:
        '''
        remove a vertex with a given name
        :vertex: the name of the vertex to addd
        :returns: True if successful
        '''
        result = super().remove_vertex(vertex)
        del self.vertex_positions[vertex]
        return result

    def add_vertex(self, vertex: str) -> bool:
        '''
        add a vertex given a name
        :vertex: the name of the vertex to add
        :returns: True if successful
        '''
        if super().add_vertex(vertex):
            self.vertex_positions[vertex] = self.get_scaled_mouse_pos()
            return True
        return False

    def add_new_vertex(self) -> str:
        '''
        add a new vertex without a given name
        :returns: name of the vertex if success or else false
        '''
        for name in self.possible_names:
            if self.contains_vertex(name):
                continue
            else:
                self.add_vertex(name)
                return name
        return None

    def clear(self):
        '''
        completely clears the graph of verticies and edges
        '''
        super().clear()
        self.vertex_positions = {}

    def rename_vertex(self, old: str, new: str) -> bool:
        '''
        renames a vertex from {old} to {new}
        :old: initial name of vertex
        :new: new name of vertex
        :returns: True if successful
        '''
        if not super().rename_vertex(old, new):
            return False
        self.vertex_positions[new] = self.vertex_positions[old]
        del self.vertex_positions[old]
        return True

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
    g.rename_vertex('a', 'frank')
    g.run()

if __name__ == "__main__":
    main()

