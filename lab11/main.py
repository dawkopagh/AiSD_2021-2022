#!/usr/bin/python
# -*- coding: utf-8 -*-

# gotowe

import numpy as np
from copy import deepcopy

class Vertex:
    def __init__(self, id):
        self.id = id

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


class Edge:
    def __init__(self, origin, target, weight=None):
        self.origin = origin
        self.target = target
        self.weight = weight


class NeighMatrix:
    def __init__(self):
        self.vertices = {}
        self.neighMatrix = None

    def insertVertex(self, vertex):
        if self.neighMatrix is None:
            self.neighMatrix = [[0]]
            self.vertices[vertex] = len(self.neighMatrix) - 1
        else:
            for inx in range(len(self.neighMatrix)):
                self.neighMatrix[inx].append(0)
            self.vertices[vertex] = len(self.neighMatrix)
            self.neighMatrix.append([0] * (len(self.neighMatrix) + 1))

    def insertEdge(self, vertex1, vertex2):
        self.neighMatrix[self.vertices[vertex1]][self.vertices[vertex2]] += 1
        self.neighMatrix[self.vertices[vertex2]][self.vertices[vertex1]] += 1

    def deleteVertex(self, vertex):
        keyFoundFlag = False
        inx = self.getVertexIDx(vertex)
        for row in range(len(self.neighMatrix)):
            self.neighMatrix[row] = self.neighMatrix[row][0:inx] + self.neighMatrix[row][inx + 1:]  # usunięcie poszczególny krawędzi

        self.neighMatrix = self.neighMatrix[:inx] + self.neighMatrix[inx + 1:]  # usunięcie węzła z macierzy sąsiedztwa

        for keys in self.vertices.keys():  # zmniejszenie indeksów elementów znajdujących się za usuwanym węzłem w słowniku
            if keys == vertex:
                keyFoundFlag = True
            if keyFoundFlag:
                self.vertices[keys] = self.vertices[keys] - 1
        del self.vertices[vertex]

    def deleteEdge(self, vertex1, vertex2):
        self.neighMatrix[self.getVertexIDx(vertex1)][self.getVertexIDx(vertex2)] -= 1  # generalnie powinniśmy odjąć 1 - usuwamy tylko jedną krawędź, ale przykład testowy dla jednej pary węzłów dwa razy wywołuje tą samą
        self.neighMatrix[self.getVertexIDx(vertex2)][self.getVertexIDx(vertex1)] -= 1  # metodę insert więc, a jako że jest to graf nieskierowany to nie do końca rozumiem takie działanie - dlatego dla potrzeby prezentacji, że krawędź faktycznie
        # znika zamiast 1 dałem 2

    def getVertexIDx(self, vertex):
        return self.vertices[vertex]

    def getVertex(self, vertex_idx):
        for keys, vals in self.vertices.items():
            if vertex_idx == vals:
                return keys

    def neighbours(self, vertex_idx):
        counter = 0
        id = self.getVertexIDx(vertex_idx)
        for inx in range(len(self.neighMatrix())):
            if self.neighMatrix[id][inx]:
                counter += 1

    def order(self):
        return len(self.neighMatrix())

    def size(self):
        numOfEdges = 0
        for row in range(len(self.neighMatrix)):
            for col in range(len(self.neighMatrix)):
                numOfEdges += self.neighMatrix[row][col - row]
        return numOfEdges

    def edges(self):
        listOfPairs = []
        for row in range(len(self.neighMatrix)):
            for col in range(len(self.neighMatrix)):
                if self.neighMatrix[row][col]:
                    listOfPairs.append((self.getVertex(row), self.getVertex(col)))
        return listOfPairs


def Ullman1(g,p, m=None, used_columns=None, current_row=0):

    if m is None:
        m = np.zeros((np.shape(p)[0], np.shape(g)[0]))
        used_columns = [0 for inx in range(np.shape(g)[0])]

    if current_row == np.shape(m)[0]:
        check = np.dot(m, np.transpose(np.dot(m,g)))
        if np.array_equal(check, p):
            Ullman1.num_of_isomorphisms += 1
            return True

    m_c = deepcopy(m)

    for inx in range(len(used_columns)):
        if used_columns[inx] == 0 and current_row < np.shape(m)[0]:
            for col in range(np.shape(m)[1]):
                if used_columns[col] == 0:
                    m_c[current_row, col] = 0
            m_c[current_row, inx] = 1
            used_columns[inx] = 1
            Ullman1(g,p,m_c, used_columns, current_row+1)
            Ullman1.no_recursion += 1
            used_columns[inx] = 0
    return False

def Ullman2(g,p, m=None, used_columns=None, current_row=0, m0 = None):

    if m is None:
        m = np.zeros((np.shape(p)[0], np.shape(g)[0]))
        used_columns = [0 for inx in range(np.shape(g)[0])]
        m0 = deepcopy(m)

    for row in range(np.shape(p)[0]):
        for col in range(np.shape(g)[0]):
            if sum(p[row]) <= sum(g[col]):
                m0[row,col] = 1

    if current_row == np.shape(m)[0]:
        check = np.dot(m, np.transpose(np.dot(m,g)))
        if np.array_equal(check, p):
            Ullman2.num_of_isomorphisms += 1

            return True

    m_c = deepcopy(m)

    for inx in range(len(used_columns)):
        if used_columns[inx] == 0 and current_row < np.shape(m)[0] and m0[current_row,inx] == 1:
            for col in range(np.shape(m)[1]):
                if used_columns[col] == 0:
                    m_c[current_row, col] = 0
            m_c[current_row, inx] = 1
            used_columns[inx] = 1
            Ullman2(g,p,m_c, used_columns, current_row+1, m0)
            Ullman2.no_recursion += 1
            used_columns[inx] = 0
    return False

def Prune(g, p, m, current_row):
    execute = True
    while execute:
        changed = False
        for row in range(np.shape(m)[0]):
            for col in range(np.shape(m)[1]):
                if m[row,col] == 1:
                    for p_inx in range(np.shape(p)[0]):
                        if p[row, p_inx] >= 1:
                            for g_inx in range(np.shape(g)[0]):
                                if g[col, g_inx] == 0 and m[p_inx, g_inx] == 1:
                                    m[row,col] = 0
                                    changed = True
        if not changed:
            execute = 0

    for i in m[:current_row]:
        if (i == 0).all():
            return False
    return True


def Ullman3(g, p, m=None, used_columns=None, current_row=0, m0=None):

    if m is None:
        m = np.zeros((np.shape(p)[0], np.shape(g)[0]))
        used_columns = [0 for inx in range(np.shape(g)[0])]
        m0 = deepcopy(m)

    for row in range(np.shape(p)[0]):
        for col in range(np.shape(g)[0]):
            if sum(p[row]) <= sum(g[col]):
                m0[row, col] = 1

    if current_row == np.shape(m)[0]:
        check = np.dot(m, np.transpose(np.dot(m, g)))
        if np.array_equal(check, p):
            Ullman3.num_of_isomorphisms += 1
            return True

    m_c = deepcopy(m)
    flag = Prune(g, p, m_c, current_row)
    if not flag:
        return False

    for inx in range(len(used_columns)):
        if used_columns[inx] == 0 and current_row < np.shape(m)[0] and m0[current_row, inx] == 1:
            for col in range(np.shape(m)[1]):
                if used_columns[col] == 0:
                    m_c[current_row, col] = 0
            m_c[current_row, inx] = 1
            used_columns[inx] = 1
            Ullman3(g, p, m_c, used_columns, current_row + 1, m0)
            Ullman3.no_recursion += 1
            used_columns[inx] = 0
    return False

def main():
    graph_G = [('A', 'B', 1), ('B', 'F', 1), ('B', 'C', 1), ('C', 'D', 1), ('C', 'E', 1), ('D', 'E', 1)]
    graph_P = [('A', 'B', 1), ('B', 'C', 1), ('A', 'C', 1)]

    testg = NeighMatrix()
    testp = NeighMatrix()
    vert = ["A", "B", "C", "D", "E", "F"]
    vert2 = ["A", "B", "C"]

    for v in vert2:
        testp.insertVertex(v)

    for edge in graph_P:
        testp.insertEdge(edge[0], edge[1])

    for v in vert:
        testg.insertVertex(v)

    for edge in graph_G:
        testg.insertEdge(edge[0], edge[1])

    gMatrix = np.array(testg.neighMatrix)
    pMatrix = np.array(testp.neighMatrix)

    Ullman1.num_of_isomorphisms = 0
    Ullman1.no_recursion = 0
    Ullman1(gMatrix, pMatrix)
    print(Ullman1.num_of_isomorphisms, Ullman1.no_recursion)

    Ullman2.num_of_isomorphisms = 0
    Ullman2.no_recursion = 0
    Ullman2(gMatrix, pMatrix)
    print(Ullman2.num_of_isomorphisms, Ullman2.no_recursion)

    Ullman3.num_of_isomorphisms = 0
    Ullman3.no_recursion = 0
    Ullman3(gMatrix, pMatrix)
    print(Ullman3.num_of_isomorphisms, Ullman3.no_recursion)

main()
