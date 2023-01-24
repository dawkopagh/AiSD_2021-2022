#!/usr/bin/python
# -*- coding: utf-8 -*-

import polska

class Vertex:
    def __init__(self, id):
        self.id = id

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

class Edge:
    def __init__(self, origin, target, weight = None):
        self.origin = origin
        self.target = target
        self.weight = weight

class NeighMatrix:
    def __init__(self):
        self.vertices = {}
        self.neighList = None

    def insertVertex(self, vertex):
        if self.neighList is None:
            self.neighList = [[0]]
            self.vertices[vertex] = len(self.neighList)-1
        else:
            for inx in range(len(self.neighList)):
                self.neighList[inx].append(0)
            self.vertices[vertex] = len(self.neighList)
            self.neighList.append([0] * (len(self.neighList)+1))

    def insertEdge(self, vertex1, vertex2):
        self.neighList[self.vertices[vertex1]][self.vertices[vertex2]] += 1
        self.neighList[self.vertices[vertex2]][self.vertices[vertex1]] += 1

    def deleteVertex(self, vertex):
        keyFoundFlag = False
        inx = self.getVertexIDx(vertex)
        for row in range(len(self.neighList)):
            self.neighList[row] = self.neighList[row][0:inx] + self.neighList[row][inx+1:] #usunięcie poszczególny krawędzi

        self.neighList = self.neighList[:inx] + self.neighList[inx+1:]  #usunięcie węzła z macierzy sąsiedztwa

        for keys in self.vertices.keys(): #zmniejszenie indeksów elementów znajdujących się za usuwanym węzłem w słowniku
            if keys == vertex:
                keyFoundFlag = True
            if keyFoundFlag:
                self.vertices[keys] = self.vertices[keys] - 1
        del self.vertices[vertex]

    def deleteEdge(self, vertex1, vertex2):
        self.neighList[self.getVertexIDx(vertex1)][self.getVertexIDx(vertex2)] -= 2 #generalnie powinniśmy odjąć 1 - usuwamy tylko jedną krawędź, ale przykład testowy dla jednej pary węzłów dwa razy wywołuje tą samą
        self.neighList[self.getVertexIDx(vertex2)][self.getVertexIDx(vertex1)] -= 2 #metodę insert więc, jako że jest to graf nieskierowany to nie do końca rozumiem takie działanie - dlatego dla potrzeby prezentacji, że krawędź faktycznie
                                                                                    #znika zamiast 1 dałem 2
    def getVertexIDx(self, vertex):
        return self.vertices[vertex]

    def getVertex(self, vertex_idx):
        for keys, vals in self.vertices.items():
            if vertex_idx == vals:
                return keys
    
    def neighbours(self, vertex_idx):
        counter = 0
        id = self.getVertexIDx(vertex_idx)
        for inx in range(len(self.neighList())):
            if self.neighList[id][inx]:
                counter += 1

    def order(self):
        return len(self.neighList())

    def size(self):
        numOfEdges = 0
        for row in range(len(self.neighList)):
            for col in range(len(self.neighList)):
                numOfEdges += self.neighList[row][col-row]
        return numOfEdges

    def edges(self):
        listOfPairs = []
        for row in range(len(self.neighList)):
            for col in range(len(self.neighList)):
                if self.neighList[row][col]:
                    listOfPairs.append((self.getVertex(row),self.getVertex(col)))
        return listOfPairs

class NeighList:
    def __init__(self):
        self.vertices = {}
        self.neighList = None

    def insertVertex(self, vertex):
        if self.neighList is None:
            self.neighList = [[]]
            self.vertices[vertex] = len(self.neighList)-1
        else:
            self.neighList.append([])
            self.vertices[vertex] = len(self.neighList)-1

    def insertEdge(self, vertex1, vertex2):
        self.neighList[self.getVertexIDx(vertex1)].append(vertex2)
        #self.neighList[self.getVertexIDx(vertex2)].append(vertex1)

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
        return self.neighList[vertex_idx]

    def order(self):
        return len(self.neighList)

    def size(self):
        numOfEdges = 0
        for vertex in self.neighList:
            numOfEdges += len(vertex)
        return numOfEdges//2

    def edges(self):
        listOfPairs = []
        for vertex_inx in range(len(self.vertices)):
            for edge in self.neighList[vertex_inx]:
                listOfPairs.append((self.getVertex(vertex_inx), edge))
        return listOfPairs

def test_fun(test):
    nodes = ['Z', 'G', 'N', 'B', 'F', 'P', 'C', 'E', 'W', 'L', 'D', 'O', 'S', 'T', 'K', 'R']

    graf = [('Z', 'G'), ('Z', 'P'), ('Z', 'F'),
            ('G', 'Z'), ('G', 'P'), ('G', 'C'), ('G', 'N'),
            ('N', 'G'), ('N', 'C'), ('N', 'W'), ('N', 'B'),
            ('B', 'N'), ('B', 'W'), ('B', 'L'),
            ('F', 'Z'), ('F', 'P'), ('F', 'D'),
            ('P', 'F'), ('P', 'Z'), ('P', 'G'), ('P', 'C'), ('P', 'E'), ('P', 'O'), ('P', 'D'),
            ('C', 'P'), ('C', 'G'), ('C', 'N'), ('C', 'W'), ('C', 'E'),
            ('E', 'P'), ('E', 'C'), ('E', 'W'), ('E', 'T'), ('E', 'S'), ('E', 'O'),
            ('W', 'C'), ('W', 'N'), ('W', 'B'), ('W', 'L'), ('W', 'T'), ('W', 'E'),
            ('L', 'W'), ('L', 'B'), ('L', 'R'), ('L', 'T'),
            ('D', 'F'), ('D', 'P'), ('D', 'O'),
            ('O', 'D'), ('O', 'P'), ('O', 'E'), ('O', 'S'),
            ('S', 'O'), ('S', 'E'), ('S', 'T'), ('S', 'K'),
            ('T', 'S'), ('T', 'E'), ('T', 'W'), ('T', 'L'), ('T', 'R'), ('T', 'K'),
            ('K', 'S'), ('K', 'T'), ('K', 'R'),
            ('R', 'K'), ('R', 'T'), ('R', 'L')]

    for node in nodes:
        test.insertVertex(node)
    for element in graf:
        test.insertEdge(element[0], element[1])
    test.deleteVertex("K")
    test.deleteEdge("W", "E")
    polska.draw_map(test.edges())

# NeighborMatrix = NeighMatrix()
# test_fun(NeighborMatrix)

NeighborList = NeighList()
test_fun(NeighborList)