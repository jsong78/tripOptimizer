parent = dict()
rank = dict()


def make_set(vertice):
    parent[vertice] = vertice
    rank[vertice] = 0


def find(vertice):
    if parent[vertice] != vertice:
        parent[vertice] = find(parent[vertice])
    return parent[vertice]


def union(vertice1, vertice2):
    root1 = find(vertice1)
    root2 = find(vertice2)
    if root1 != root2:
        if rank[root1] > rank[root2]:
            parent[root2] = root1
        else:
            parent[root1] = root2
        if rank[root1] == rank[root2]: rank[root2] += 1


def kruskal(graph, visited):
    temp_edges = []
    for edge in graph.edges():
        if edge.source not in visited:
            if edge.dest not in visited:
                temp_edges.append(edge)
    for vertice in graph.vertices():
        make_set(vertice)
        minimum_spanning_tree = []
        #edges = list(graph.edges())
        temp_edges.sort(key = lambda x : x.weight)
    # print edges
    for edge in temp_edges:
        if edge not in minimum_spanning_tree:
            vertice1 = edge.source
            vertice2 = edge.dest
            if find(vertice1) != find(vertice2):
                union(vertice1, vertice2)
                minimum_spanning_tree.append(edge)

    result = sorted(minimum_spanning_tree, key = lambda x: x.weight)
    # print("MST-------------------------------------------------------")
    # for edge in result:
    #     print(edge.source)
    #     print(edge.dest)
    #     print(edge.weight)
    #     print("-"*50)
    return sorted(minimum_spanning_tree, key = lambda x: x.weight)

def mstCost(graph, visited):

    sol = kruskal(graph, visited)
    sum = 0.0
    for edge in sol:
        sum += float(edge.weight)

    return sum