#!/usr/bin/env python3

from graph import Graph

def test_graph(g: Graph, title: str = ''):
    '''tests a graph'''
    print(title, end='')
    print(g)
    print(list(g._get_all_adjavent_verticies('a')))
    print(g.get_adjacent_verticies('a'))
    print(g.get_paths())

def main():
    '''driver code'''
    sep = '-' * 40
    test_graph(Graph.build(
        {'a', 'b', 'c', 'd'},
        [
            {'a', 'b'},
            {'b', 'c'},
            {'a', 'c'},
            {'c', 'd'},
            {'a', 'd'}
        ]
    ), f'{sep}graph 1{sep}\n')
    test_graph(Graph.build(
        {'a', 'b'},
        [
            {'a', 'b'},
            {'a', 'b'}
        ]
    ), f'{sep}graph 2{sep}\n')

if __name__ == "__main__":
    main()
