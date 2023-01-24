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
        return(self.rows, self.cols)

    def __add__(self, other):
        if self.__len__() == other.__len__():
            result = Matrix((self.rows, self.cols))
            for row in range(self.rows):
                current_row = other.__getitem__(row)
                for col in range(self.cols):
                    result[row][col] += current_row[col] + self.matrix[row][col]
            return result

    def __mul__(self, other):
        if self.cols == other.rows:
            result = Matrix((self.rows, other.cols))
            for row in range(result.rows):
                for col in range(result.cols):
                    for inx in range(self.cols):
                        result[row][col] += self.matrix[row][inx] * other.matrix[inx][col]
            return result

    def __str__(self) -> None:
        result = ''
        for row in range(self.rows):
            result += str(self.matrix.__getitem__(row)) + "\n"
        return result

def transpose(matrix: Matrix):
    result = Matrix((matrix.cols, matrix.rows))
    for row in range(matrix.rows):
        for col in range(matrix.cols):
            result[col][row] = matrix[row][col]
    return result


a_matrix = Matrix([[1, 0, 2],
  [-1, 3, 1]])

size = (2,3)
b_matrix = Matrix(size,1)

c_matrix = Matrix([[3, 1],
  [2, 1],
  [1, 0]])

print(transpose(a_matrix))
print(a_matrix+b_matrix)
print(a_matrix*c_matrix)