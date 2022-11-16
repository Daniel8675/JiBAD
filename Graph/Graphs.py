import collections


class Graph:  # Klasa implementuje graf prosty (tzn. nie ma krawedzi skierowanych, jak i multi-krawedzi pomiedzy
    # wierzcholkami)

    def __init__(self, graph=None):  # inicjalizacja grafu z możliwością podania już gotowego grafu w formie słownika
        if graph is None:
            graph = {}

        if type(graph) is dict or type(graph) is Graph:
            self._graph = graph
        else:
            raise ValueError("Graph must be dict!!!")

    def __str__(self):
        return str(self._graph)

    def add_vertex(self, vertex):
        self.is_vertex_correct(vertex)
        self._graph.setdefault(vertex, [])

    def add_edge(self, edge):
        vertex_s, vertex_e = self.is_edge_correct(edge)

        self.is_vertex_exist(vertex_s)
        self.is_vertex_exist(vertex_e)

        try:  # krawedz dodajemy tylko wtedy gdy takowa nie istnieje wynika to z faktu ze implementujemy graf prosty
            if not self.is_edge_exist((vertex_s, vertex_e)):
                pass
        except KeyError:
            self._graph[vertex_s].append(vertex_e)
            self._graph[vertex_e].append(vertex_s)

    def remove_edge(self, edge):
        vertex_s, vertex_e = self.is_edge_correct(edge)

        self.is_vertex_exist(vertex_e)
        self.is_vertex_exist(vertex_s)
        self.is_edge_exist(edge)

        self._graph[vertex_s].remove(vertex_e)
        self._graph[vertex_e].remove(vertex_s)

    def neighbors(self, vertex):
        self.is_vertex_exist(vertex)

        return list(self._graph[vertex])  # raz jeszcze dziekuje za uporanie sie z bugiem

    def remove_vertex(self, vertex):
        self.is_vertex_exist(vertex)

        for neighbor in self.neighbors(vertex):
            self.remove_edge([neighbor, vertex])

        del self._graph[vertex]

    def bfs(self, root):
        self.is_vertex_exist(root)
        return BfsIterator(self, root)

    def dfs(self, root):
        self.is_vertex_exist(root)
        return DfsIterator(self, root)

    @staticmethod
    def is_edge_correct(edge):
        try:
            vertex_s, vertex_e = list(edge)
            return vertex_s, vertex_e
        except ValueError:
            raise ValueError("You gave the wrong edge!!! The edge should look like: (vertex1, vertex2)")

    @staticmethod
    def is_vertex_correct(vertex):
        if type(vertex) is int or type(vertex) is str or type(vertex) is tuple:
            return True
        else:
            raise TypeError("Vertex must be int, str or tuple!!!")

    def is_edge_exist(self, edge):
        vertex_s, vertex_e = self.is_edge_correct(edge)
        if vertex_e in self._graph.get(vertex_s) and vertex_s in self._graph.get(vertex_e):
            return True
        else:
            raise KeyError("Edge does not exist!!!")

    def is_vertex_exist(self, vertex):
        self.is_vertex_correct(vertex)
        if self._graph.get(vertex) is not None:
            return True
        else:
            raise KeyError("Vertex does not exist!!!")


class BfsIterator(Graph):

    def bfs(self, root):
        visited, queue = [root], collections.deque([root])

        while queue:
            vertex = queue.popleft()
            for neighbors in self._graph.neighbors(vertex):
                if neighbors not in visited:
                    visited.append(neighbors)
                    queue.append(neighbors)

        return visited

    def __init__(self, graph, root):
        super().__init__(graph)
        self.root = root
        self._order = collections.deque(self.bfs(self.root))

    def __next__(self):
        try:
            return self._order.popleft()
        except IndexError:
            raise StopIteration

    def __iter__(self):
        return self


class DfsIterator(Graph):
    def dfs(self, root, visited=None):
        if visited is None:
            visited = []
        visited.append(root)

        for neighbor in self._graph.neighbors(root):
            if neighbor not in visited:
                self.dfs(neighbor, visited)

        return visited

    def __init__(self, graph, root):
        super().__init__(graph)
        self.root = root
        self._order = collections.deque(self.dfs(self.root))

    def __next__(self):
        try:
            return self._order.popleft()
        except IndexError:
            raise StopIteration

    def __iter__(self):
        return self


# a = Graph()
# a.add_vertex(1)
# a.add_vertex(2)
# a.add_vertex(3)
# a.add_vertex(4)
# a.add_vertex(5)
# a.add_vertex(6)
# a.add_vertex(7)
# a.add_vertex(8)
# a.add_vertex(9)
# a.add_vertex(10)
# a.add_edge((1, 2))
# a.add_edge((1, 5))
# a.add_edge((1, 9))
# a.add_edge((2, 4))
# a.add_edge((2, 3))
# a.add_edge((3, 4))
# a.add_edge((5, 7))
# a.add_edge((5, 6))
# a.add_edge((5, 8))
# a.add_edge((10, 8))
# a.add_edge((10, 9))
#
# print(a)
#
# for i in a.bfs(1):
#     print(i)
#
# for i in a.dfs(5):
#     print(i)
