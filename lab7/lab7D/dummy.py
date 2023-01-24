#!/usr/bin/python
# -*- coding: utf-8 -*-

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
        self.neighList[self.getVertrexIDx(vertex2)].append(vertex1)

    def deleteVertex(self, vertex):
        keyFoundFlag = False

        for node in self.neighList:
            node.remove(vertex)

        for keys in self.vertices.keys():  # zmniejszenie indeksów elementów znajdujących się za usuwanym węzłem w słowniku
            if keys == vertex:
                keyFoundFlag = True
            if keyFoundFlag:
                self.vertices[keys] = self.vertices[keys] - 1
        del self.vertices[vertex]

    def deleteEdge(self, vertex1, vertex2):
        self.neighList[self.getVertexIdx(vertex1)].remove(vertex2)
        self.neighList[self.getVertexIdx(vertex2)].remove(vertex1)

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
        for vertex in self.neighList:
            for edge in vertex:
                listOfPairs.append(vertex, edge)
        return listOfPairs