#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import matplotlib
from matplotlib import pyplot as plt

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

def main():
    I = cv2.imread('sample.png', cv2.IMREAD_GRAYSCALE)
    test = NeighList()

    for row in range(len(I)):
        for col in range(len(I[0])):

            test.insertVertex(Vertex(len(I)*col+row, I[row,col]))

    for row in range(1, len(I)-1):
        for col in range(1, len(I[0])-1):
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i != 0 and j != 0:
                        test.insertEdge(Vertex(len(I)*col+row, I[row,col]), Vertex(len(I)*(col-j)+row-i, I[row-i,col-j]), abs(I[row,col] - I[row-i,col-j]))

    result = PrimMST(test,0)

    max_weight = 0
    edge_inx = -1

    for vertex in range(len(result.neighList)):
        for edge in range(len(result.neighList[vertex])):
            if result.neighlist[vertex,edge].weight > max_weight:
                edge_inx = vertex+edge

main()

