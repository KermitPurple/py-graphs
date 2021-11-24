from typing import Set, List

class Graph():
    '''
    This class represents the mathematical concept of a graph
    A vertex is a string representing the name of the vertex
    An edge is a set of two verticies
    '''
    def __init__(self):
        self.vertices = set()
        self.edges = []

    def __str__(self):
        return f'Graph(V={self.vertices}, E={self.edges})'

    @classmethod
    def build(cls, vertices: Set[str], edges: List[Set[str]]) -> 'Graph':
        '''
        builds a graph from the given verticies and edges
        '''
        g = cls()
        for vertex in vertices:
            g.add_vertex(vertex)
        for edge in edges:
            g.add_edge(*edge)
        return g

    def contains_vertex(self, vertex: str) -> bool:
        '''
        checks if a vertex is in the verticies
        :vertex: the vertex to check
        :returns: True if the vertex exists in self.vertices
        '''
        return vertex in self.vertices

    def add_vertex(self, vertex: str) -> bool:
        '''
        adds a new vertex to the graph
        :vertex: the vertex to add
        :returns: True if it was successfully added
        '''
        if self.contains_vertex(vertex):
            return False
        self.vertices.add(vertex)
        return True

    def remove_vertex(self, vertex: str) -> bool:
        '''
        :returns: True if the vertex was successfully removed
        '''
        if not self.contains_vertex(vertex):
            return False
        self.vertices.remove(vertex)
        i = 0
        while i < len(self.edges):
            if vertex in self.edges[i]:
                self.edges.pop(i)
            else:
                i += 1
        return True

    def contains_edge(self, vertex1: str, vertex2: str) -> bool:
        '''
        checks if an edge exists in the graph
        :vertex1: one of the points of the edge
        :vertex2: the other point of the edge
        :returns: True if the edge already exists
        '''
        return {vertex1, vertex2} in self.edges

    def add_edge(self, vertex1: str, vertex2: str) -> bool:
        '''
        adds a new edge to the graph
        :vertex1: one of the points of the edge
        :vertex2: the other point of the edge
        :returns: True if successfully added
        '''
        if vertex1 in self.vertices and vertex2 in self.vertices:
            self.edges.append({vertex1, vertex2})
            return True
        return False

    def remove_edge(self, vertex1: str, vertex2: str) -> bool:
        '''
        removes an edge from the graph
        :vertex1: one of the points of the edge
        :vertex2: the other point of the edge
        :returns: True if successfully removed
        '''
        edge = {vertex1, vertex2}
        if edge not in self.edges:
            return False
        self.edges.remove(edge)
        return True

    def get_adjacent_verticies(self, vertex: str) -> Set[str]:
        '''
        returns adjacent vertecies
        :vertex: the vertex to check
        :returns: a set of verticies adjacent to the given vertex
        '''
        return set(self._get_all_adjavent_verticies(vertex))

    def _get_all_adjavent_verticies(self, vertex: str) -> map:
        '''
        returns adjacent vertecies
        :vertex: the vertex to check
        :returns: a map of verticies adjacent to the given vertex
        '''
        return map(lambda edge: (edge - {vertex}).pop(), filter(lambda edge: vertex in edge, self.edges))

    def get_paths(self) -> List[str]:
        '''
        gets all possible paths in the graph
        :returns: a list of verticies
        '''
        def get_paths_helper(path: List[str]):
            size = len(path)
            if size == 0:
                return []
            elif size == 1:
                result = []
            else:
                result = [path]
            end = path[-1]
            for v in self._get_all_adjavent_verticies(end):
                if v not in path:
                    result += get_paths_helper(path + [v])
            return result
        result = []
        for vertex in self.vertices:
            result += get_paths_helper([vertex])
        return result
