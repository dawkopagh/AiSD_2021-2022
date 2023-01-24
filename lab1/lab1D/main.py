#!/usr/bin/python
# -*- coding: utf-8 -*-


class Matrix:
    def __init__(self, arg, val = 0) -> None:
        if(isinstance(arg, tuple)):
            self.rows = arg[0]
            self.cols = arg[1]
            self.matrix = [[val for col in range(self.cols)] for row in range(self.rows)]
        else:
            self.rows = len(arg)
            self.cols = len(arg[0])
            self.matrix = arg

    def __getitem__(self, row):
        return self.matrix[row]

    def __len__(self):
        return(len(self.matrix), len(self.matrix[0]))

    def __add__(self, other):
        if self.__len__() == other.__len__():
            result = Matrix((self.rows, self.cols))
            for row in range(self.rows):
                current_row = other.__getitem__(row)
                for col in range(self.cols):
                    result[row][col] += current_row[col] + self.matrix[row][col]
            return result

    def __mul__(self, other):
        other_matrix = Matrix(other)
        if self.cols == other_matrix.rows:
            result = Matrix((self.rows, other_matrix.cols))
            for row in range(result.rows):
                for col in range(result.cols):
                    for inx in range(self.cols):
                        result[row][col] += self.matrix[row][inx] * other_matrix.matrix[inx][col]
            return result

    def __str__(self) -> None:
        for row in range(self.rows):
            print(self.matrix.__getitem__(row))

def transpose(matrix: Matrix):
    result = Matrix((matrix.cols, matrix.rows))
    for row in range(matrix.rows):
        for col in range(matrix.cols):
            result[col][row] = matrix[row][col]
    return result

def det2x2(matrix :Matrix) -> float:
    return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]

def chio(matrix: Matrix) -> float:
    if matrix.rows == matrix.cols:
        NO_OPPOSED_SIGN = 1
        if matrix[0][0] == 0:
            for row in range(matrix.rows):
                if row[0] != 0:
                    buff = matrix[0]
                    matrix[0] = matrix[row]
                    matrix[row] = buff
                    NO_OPPOSED_SIGN = -1
        if matrix.rows >= 2:
            a1 = matrix[0][0]
            result = Matrix((matrix.rows-1, matrix.cols-1))
            for row in range(matrix.rows-1):
                for col in range(matrix.cols-1):
                    result[row][col] = det2x2(Matrix([[a1,matrix[0][col+1]],
                                                    [matrix[row+1][0], matrix[row+1][col+1]]]))
            det = chio(result)/a1**(matrix.rows-2)
            return det
        return matrix[0][0] * NO_OPPOSED_SIGN


dummy = Matrix([
[5 , 1 , 1 , 2 , 3],
[4 , 2 , 1 , 7 , 3],
[2 , 1 , 2 , 4 , 7],
[9 , 1 , 0 , 7 , 0],
[1 , 4 , 7 , 2 , 2]
])

dummy2 = Matrix(
    [
        [4, 2, 1, 7, 3,1],
        [0, 1, 1, 2, 3],
        [2, 1, 2, 4, 7],
        [1, 4, 7, 2, 2],
        [9, 1, 0, 7, 0]
    ]
)

print("Wyznacznik pierwszej macierzy: ", chio(dummy))
print("Wyznacznik drugiej macierzy: ", chio(dummy2))

# W celu obliczenia wyznacznika drugiej macierzy musimy tą macierz przekształcić w taki sposób, żeby pierwszy element pierwszego wiersza
# był różny od zera. Możemy skorzystać z własności operowania na macierzach - przy zamianie wierszy miejscami wartość wyznacznika co do modułu pozostaje taka sama,
# zmienia się jedynie jego znak. W podanym przykładzie jest to sposób wystarczający. Jeśli jednak okazałoby się, że wszystkie wiersze zaczynają się od zera, to można jeszcze
# dodać funkcjonalność która wykonuje transpozycję tej macierzy i ponownie sprawdza pierwsze wyrazy wierszy (byłyby to po prostu kolejne elementy pierwszego wiersza macierzy zadanej) w takim przypadku
# ponownie korzystając z własności działania na macierzach - wyznacznik macierzy i wyznacznik jej transpozycji są sobie równe.

