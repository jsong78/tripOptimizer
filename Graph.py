import sys

class Edge():
    source = None
    dest = None
    weight = 1

    def __init__(self, source, dest, weight):
        self.source = source
        self.dest = dest
        self.weight = weight

    def __eq__(self, other):
        return (self.source == other.source and self.weight == other.weight and self.dest == other.dest) or (self.source == other.dest and self.dest == other.source and self.weight == other.weight)



class PNode():
    def __init__(self,address,closest_rest):
        #self.x_coord = x_coord
        #self.y_coord = y_coord
        self.address = address
        self.closest_rest = closest_rest

    def markvisit(self):
        self.visited = True

    def setprev(self,prev):
        self.prev = prev

    def setDist(self,dist):
        self.distance = dist


class Graph(object):



    '''class GNode():
        graph = []
        avg_x_coord = 0.0
        avg_y_coord = 0.0
        def __init__(self, graph=None):
            self.graph = []
            self.avg_x_coord = 0.0
            self.avg_y_coord = 0.0

        def add'''

    def __init__(self, graph_dict=None):
        """ initializes a graph object
            If no dictionary or None is given,
            an empty dictionary will be used
        """
        self.edgelist = []
        if graph_dict == None:
            graph_dict = {}
        self.__graph_dict = graph_dict

    def vertices(self):
        """ returns the vertices of a graph """
        return list(self.__graph_dict.keys())

    def edges(self):
        """ returns the edges of a graph """
        return self.__generate_edges()

    def get_edges(self, vertex):
        return self.__graph_dict[vertex]
    def add_vertex(self, vertex):
        """ If the vertex "vertex" is not in
            self.__graph_dict, a key "vertex" with an empty
            list as a value is added to the dictionary.
            Otherwise nothing has to be done.
        """
        if vertex not in self.__graph_dict:
            self.__graph_dict[vertex] = []

    def add_edge(self, vertex1,vertex2, weight):
        edge = Edge(vertex1, vertex2, weight)
        if vertex1 in self.__graph_dict:
            if edge not in self.__graph_dict[vertex1]:
                self.__graph_dict[vertex1].append(edge)
        else:
            if edge not in self.__graph_dict[vertex1]:
                self.__graph_dict[vertex1] = [edge]

        if vertex2 in self.__graph_dict:
            if edge not in self.__graph_dict[vertex2]:
                self.__graph_dict[vertex2].append(edge)
        else:
            if edge not in self.__graph_dict[vertex1]:
                self.__graph_dict[vertex2] = [edge]

        if edge not in self.edgelist:
            self.edgelist.append(edge)

    def __generate_edges(self):
        """ A static method generating the edges of the
            graph "graph". Edges are represented as sets
            with one (a loop back to the vertex) or two
            vertices
        """
        edges = []
        for vertex in self.__graph_dict.keys():
            for edge in self.__graph_dict[vertex]:
                if edge not in edges:
                    edges.append(edge)
        return edges


    def __str__(self):
        res = "vertices: "
        for k in self.__graph_dict:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.__generate_edges():
            res += str(edge) + " "
        return res


