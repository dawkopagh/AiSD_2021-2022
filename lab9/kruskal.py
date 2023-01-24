#gotowe

from copy import deepcopy

class Vertex:
    def __init__(self, id, brightness=None):
        self.id = id
        self.brightness = brightness

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


class Edge:
    def __init__(self, origin, target, weight=None):
        self.origin = origin
        self.target = target
        self.weight = weight


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

    def insertEdge(self, vertex1, vertex2, weight):
        self.neighList[self.getVertexIDx(vertex1)].append(Edge(vertex1, vertex2, weight))
        self.neighList[self.getVertexIDx(vertex2)].append(Edge(vertex2, vertex1, weight))

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

class UnionFind():
    def __init__(self, n):
        self.parent = [inx for inx in range(n)]
        self.size = [1] * (n)
        self.n = n
        self.weight = [float('inf') for inx in range(n)]

    def find(self, v):
        if self.parent[v] == v:
            return v
        else:
            return self.find(self.parent[v])

    def union_sets(self, s1, s2, weight):
        if not self.same_component(s1, s2):
            if self.size[s1] < self.size[s2] and self.weight[s1] > weight:
                self.parent[s1] = s2
                self.size[s1] += 1
                self.weight[s1] = weight
            elif self.size[s1] > self.size[s2] and self.weight[s2] > weight:
                self.parent[s2] = s1
                self.size[s2] += 1
                self.weight[s2] = weight
            elif self.size[s2] == self.size[s1]:
                self.parent[s1] = s2
                self.size[s1] += 1
                self.weight[s1] = weight
                # if self.weight[s2] > weight and self.weight[s1] >= self.weight[s2]:
                #     self.parent[s2] = s1
                #     self.size[s2] += 1
                #     self.weight[s2] = weight
                # elif self.weight[s1] > weight and self.weight[s2] > self.weight[s1]:
                #     self.parent[s1] = s2
                #     self.size[s1] += 1
                #     self.weight[s1] = weight

    def same_component(self, s1, s2):
        root1 = self.find(s1)
        root2 = self.find(s2)
        if root1 == root2:
            return True
        else:
            return False

def printGraph(g):
    n = g.order()
    print("------GRAPH------",n)
    for i in range(n):
        v = g.getVertex(i)
        print(v.id, end = " -> ")
        nbrs = g.neighbours(i)
        for (j, w) in nbrs:
            print(g.getVertex(j).id, w, end=";")
        print()
    print("-------------------")

def Kruskal(g):

    edges = []

    for vertex in g.neighList:
        edges += vertex

    for i in range(len(edges)):
        for j in range(len(edges)-1):
            if edges[j].weight > edges[j+1].weight:
                buff = edges[j]
                edges[j] = edges[j+1]
                edges[j+1] = buff
            elif edges[j].weight == edges[j+1].weight and (g.getVertexIDx(edges[j].origin) > g.getVertexIDx(edges[j+1].origin) or g.getVertexIDx(edges[j].target) > g.getVertexIDx(edges[j+1].target)):
                buff = edges[j]
                edges[j] = edges[j + 1]
                edges[j + 1] = buff


    union = UnionFind(len(g.vertices))

    for edge in edges:
        union.union_sets(g.getVertexIDx(edge.origin), g.getVertexIDx(edge.target), edge.weight)

    result = NeighList()
    for element in g.vertices.keys():
        result.insertVertex(element)

    for inx in range(len(union.parent)):
        if inx != union.parent[inx]:
            result.insertEdge(g.getVertex(inx), g.getVertex(union.parent[inx]), union.weight[inx])

    return result


def main():
    test = NeighList()
    wezly = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

    graf = [('A', 'B', 4), ('A', 'C', 1), ('A', 'D', 4),
            ('B', 'E', 9), ('B', 'F', 9), ('B', 'G', 7), ('B', 'C', 5),
            ('C', 'G', 9), ('C', 'D', 3),
            ('D', 'G', 10), ('D', 'J', 18),
            ('E', 'I', 6), ('E', 'H', 4), ('E', 'F', 2),
            ('F', 'H', 2), ('F', 'G', 8),
            ('G', 'H', 9), ('G', 'J', 8),
            ('H', 'I', 3), ('H', 'J', 9),
            ('I', 'J', 9)
            ]
    for element in wezly:
        test.insertVertex(Vertex(element))
    for element in graf:
        test.insertEdge(Vertex(element[0]), Vertex(element[1]), element[2])
    # stp = PrimMST(test,2)
    # printGraph(stp)

    a = Kruskal(test)

    printGraph(a)

if __name__ == "__main__":
    main()
