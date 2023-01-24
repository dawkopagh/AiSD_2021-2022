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
        #return self.neighList[vertex_idx]
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

def PrimMST(G, start_vert):
    structureMST = NeighList()
    intree = [0] * len(G.vertices)
    distance = [float('inf')] * len(G.vertices)
    parent = [-1] * len(G.vertices)

    for element in G.vertices.keys():
        structureMST.insertVertex(element)

    vertex_id = start_vert

    while intree[vertex_id] == 0:
        intree[vertex_id] = 1
        for neighbours in G.neighList[vertex_id]:
            parent_inx = structureMST.getVertexIDx(neighbours.target)
            if neighbours.weight < distance[parent_inx] and intree[parent_inx] == 0:
                distance[parent_inx] = neighbours.weight
                parent[parent_inx] = vertex_id
        if parent[vertex_id] != -1:  # chyba here blad ale idk
            structureMST.insertEdge(structureMST.getVertex(vertex_id), structureMST.getVertex(parent[vertex_id]), distance[vertex_id])

        min = float('inf')
        for inx in range(len(distance)):
            if distance[inx] < min and intree[inx] == 0:
                min = distance[inx]
                vertex_id = inx

    return structureMST

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
    stp = PrimMST(test,2)
    printGraph(stp)

if __name__ == "__main__":
    main()
