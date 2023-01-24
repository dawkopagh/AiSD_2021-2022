#gotowe

class Vertex:
    def __init__(self, id, brightness=None):
        self.id = id
        self.brightness = brightness

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


class Edge:
    def __init__(self, origin, target, capacity=None, isResidual = False):
        self.origin = origin
        self.target = target
        self.weight = capacity
        self.flow = 0
        self.residual = capacity
        self.isResidual = isResidual

    def __repr__(self):
        result = str(self.weight) + " " + str(self.flow) + " " + str(self.residual) + " " + str(self.isResidual)
        return result

class NeighList:
    def __init__(self):
        self.vertices = {}
        self.neighList = None

    def insertVertex(self, vertex):
        if self.neighList is None:
            self.neighList = [[]]
            self.vertices[vertex] = len(self.neighList) - 1
        else:
            self.neighList.append([])
            self.vertices[vertex] = len(self.neighList) - 1

    def insertEdge(self, vertex1, vertex2, capacity, isResidual):
        self.neighList[self.getVertexIDx(vertex1)].append(Edge(vertex1, vertex2, capacity, isResidual))
        self.neighList[self.getVertexIDx(vertex2)].append(Edge(vertex2, vertex1, 0, True))


    def deleteVertex(self, vertex):
        keyFoundFlag = False
        inx = self.getVertexIDx(vertex)

        for node in self.neighList:
            if vertex in node:
                node.remove(vertex)

        self.neighList = self.neighList[:inx] + self.neighList[inx + 1:]

        for keys in self.vertices.keys():  # zmniejszenie indeksów elementów znajdujących się za usuwanym węzłem w słowniku
            if keys == vertex:
                keyFoundFlag = True
            if keyFoundFlag:
                self.vertices[keys] = self.vertices[keys] - 1
        del self.vertices[vertex]

    def deleteEdge(self, vertex1, vertex2):
        self.neighList[self.getVertexIDx(vertex1)].remove(vertex2)
        self.neighList[self.getVertexIDx(vertex2)].remove(vertex1)

    def getVertexIDx(self, vertex):
        return self.vertices[vertex]

    def getVertex(self, vertex_idx):
        for keys, vals in self.vertices.items():
            if vertex_idx == vals:
                return keys

    def neighbours(self, vertex_idx):
        neighs = []
        for neighbour in self.neighList[vertex_idx]:
            neighs.append(((self.getVertexIDx(neighbour.target)), neighbour.weight))
        return neighs

    def order(self):
        return len(self.neighList)

    def size(self):
        numOfEdges = 0
        for vertex in self.neighList:
            numOfEdges += len(vertex)
        return numOfEdges // 2

    def edges(self):
        listOfPairs = []
        for vertex_inx in range(len(self.vertices)):
            for edge in self.neighList[vertex_inx]:
                listOfPairs.append((self.getVertex(vertex_inx), edge))
        return listOfPairs

def BFS(g):
    visited = len(g.vertices) * [0]
    parent = len(g.vertices) * [-1]
    queue = []
    vertex_inx = 0
    queue.append(g.getVertex(vertex_inx))

    while len(queue) > 0:
        vertex_inx = g.getVertexIDx(queue.pop(0))
        for neighbour in g.neighList[vertex_inx]:
            if visited[g.getVertexIDx(neighbour.target)] == 0 and neighbour.residual > 0 and not neighbour.isResidual:
                queue.append(neighbour.target)
                visited[g.getVertexIDx(neighbour.target)] = 1
                parent[g.getVertexIDx(neighbour.target)] = vertex_inx
    return parent

def path_analysis(g, origin, target, parent):
    vertex_inx = target
    min_capacity = float('inf')

    if parent[vertex_inx] == -1:
        return 0

    while vertex_inx != origin:
        for edge in g.neighList[parent[vertex_inx]]:
            if edge.target == g.getVertex(vertex_inx) and not edge.isResidual and edge.residual < min_capacity:
                min_capacity = edge.residual
        vertex_inx = parent[vertex_inx]
    return min_capacity

def path_augmentation(g, origin, target, parent, min_capacity):
    vertex_inx = target

    if parent[vertex_inx] == -1:
        return 0

    while vertex_inx != origin:
        for edge in g.neighList[parent[vertex_inx]]:
            if edge.target == g.getVertex(vertex_inx) and not edge.isResidual:
                edge.flow += min_capacity
                edge.residual -= min_capacity
        for edge in g.neighList[vertex_inx]:
            if g.getVertexIDx(edge.target) == parent[vertex_inx] and edge.isResidual:
                edge.residual += min_capacity
        vertex_inx = parent[vertex_inx]

def FordFulkerson(g):
    flow = 0
    vertices = []
    for vertex in g.vertices.keys():
        vertices.append(g.getVertexIDx(vertex))

    parent_list = BFS(g)
    if parent_list[g.getVertexIDx('t')] == -1:
        return 0

    min_capacity = path_analysis(g, vertices[0], vertices[g.getVertexIDx('t')], parent_list)

    while min_capacity > 0:
        path_augmentation(g, vertices[0], vertices[g.getVertexIDx('t')], parent_list, min_capacity)
        parent_list = BFS(g)
        min_capacity = path_analysis(g, vertices[0], vertices[g.getVertexIDx('t')], parent_list)

    for edges in g.neighList[g.getVertexIDx('t')]:
        flow += edges.residual

    return g, flow

def printGraph(g):
    n = g.order()
    print("------GRAPH------",n)
    for i in range(n):
        v = g.getVertex(i)
        print(v, end = " -> ")
        for edge in g.neighList[i]:
            print(edge.target, repr(edge), end=';')
        print()
    print("-------------------")

def test(graf):
    vertices = []
    for element in graf:
        if element[0] not in vertices:
            vertices.append(element[0])
        if element[1] not in vertices:
            vertices.append(element[1])

    g = NeighList()

    for element in vertices:
        g.insertVertex(element)

    for edge in graf:
        g.insertEdge(edge[0], edge[1], edge[2], False)

    g, flow = FordFulkerson(g)
    print(flow)
    printGraph(g)


graf_0 = [ ('s','u',2), ('u','t',1), ('u','v',3), ('s','v',1), ('v','t',2)]
test(graf_0)
graf_1 = [ ('s', 'a', 16), ('s', 'c', 13), ('a', 'c', 10), ('c', 'a', 4), ('a', 'b', 12), ('b', 'c', 9), ('b', 't', 20), ('c', 'd', 14), ('d', 'b', 7), ('d', 't', 4) ]
test(graf_1)
graf_2 = [ ('s', 'a', 3), ('s', 'c', 3), ('a', 'b', 4), ('b', 's', 3), ('b', 'c', 1), ('b', 'd', 2), ('c', 'e', 6), ('c', 'd', 2), ('d', 't', 1), ('e', 't', 9)]
test(graf_2)
graf_3 = [('s', 'a', 8), ('s', 'd', 3), ('a', 'b', 9), ('b', 'd', 7), ('b', 't', 2), ('c', 't', 5), ('d', 'b', 7), ('d', 'c', 4)]
test(graf_3)