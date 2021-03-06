#!/usr/bin/env python3 -i

from typing import Set, List
from draw_graph import DisplayGraph
import pygame

def draw_new_graph(verticies: Set[str] = set(), edges: List[Set[str]] = []):
    '''
    create new graph and render it
    :verticies: a set of strings representing the verticies of the graph
    :edges: a list of sets of strings representing the edges
    '''
    DisplayGraph.build(verticies, edges).run()
    pygame.quit()

d = draw_new_graph

if __name__ == "__main__":
    help(draw_new_graph)
    print('use \'draw_new_graph\' or \'d\' function to create a graph')
