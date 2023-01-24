import math
from copy import copy

MAXELEMENTS = 6

class Element:
    def __init__(self):
        self.data = [None for i in range(MAXELEMENTS)]
        self.next = None
        self.numElements = 0

    def insert(self, el, inx):
        if inx < MAXELEMENTS and self.numElements < MAXELEMENTS:
            if self.data[inx] is not None:
                self.data[inx+1:MAXELEMENTS] = self.data[inx:MAXELEMENTS-1]
                self.data[inx] = el
                self.numElements += 1
            else:
                self.data[self.numElements] = el
                self.numElements += 1
        elif inx > MAXELEMENTS and self.next is None and self.numElements < MAXELEMENTS:
            if inx > self.numElements:
                self.data[self.numElements] = el
                self.numElements += 1
        else:
            halfRange = int(MAXELEMENTS/2)
            NewNode = Element()
            NewNode.data[0:halfRange] = self.data[halfRange:]
            self.numElements = halfRange
            NewNode.numElements = halfRange
            self.data[halfRange:] = [None for i in range(halfRange)]
            if inx < halfRange:
                self.insert(el,inx)
            else:
                NewNode.insert(el,inx-halfRange)
            NewNode.next = self.next
            self.next = NewNode

class UnrolledLinkedList:
    def __init__(self):
        self.head = Element()

    def get(self, inx):
        currentList = self.head
        while currentList is not None:
            if inx >= 0 and inx <= currentList.numElements - 1:
                return currentList.data[inx%(MAXELEMENTS-1)]
            else:
                inx -= currentList.numElements
                if currentList.next is not None:
                    currentList = currentList.next
        return "asd"

    def insert(self, el, inx) -> None:
        currentList = self.head
        while currentList is not None:
            if inx >= 0 and inx <= currentList.numElements:
                currentList.insert(el, inx)
                break
            else:
                inx -= currentList.numElements
                if currentList.next is not None:
                    currentList = currentList.next
                else:
                    currentList.insert(el, inx+MAXELEMENTS)
                    currentList = None

    def delete(self, inx):
        currentList = self.head
        while currentList is not None:
            if inx >= 0 and inx <= currentList.numElements - 1:
                currentList.data[inx:MAXELEMENTS-1] = currentList.data[inx+1:MAXELEMENTS-1] + [None]
                currentList.numElements -= 1
                if currentList.numElements < int(MAXELEMENTS/2) and currentList.next is not None:
                    currentList.data[currentList.numElements] = currentList.next.data[0]
                    currentList.next.data[:MAXELEMENTS - 1] = currentList.next.data[1:MAXELEMENTS - 1] + [None]
                    currentList.numElements += 1
                    currentList.next.numElements -= 1
                    if currentList.next.numElements < int(MAXELEMENTS/2):
                        buff = currentList.next.data[0:currentList.next.numElements]
                        currentList.data[currentList.numElements:currentList.numElements+len(buff)] = buff
                        currentList.numElements += currentList.next.numElements
                        if currentList.next.next is not None:
                            currentList.next = currentList.next.next
                            break
                        else:
                            currentList.next = None
                            break
                else:
                    break

            else:
                inx -= currentList.numElements
                if currentList.next is not None:
                    currentList = currentList.next

    def __str__(self):
        txt = '[ '
        currentList = self.head
        while currentList is not None:
            if currentList.next is None:
                for inx in range(MAXELEMENTS):
                    txt += str(currentList.data[inx]) + " "
                txt += ']'
                return txt
            for inx in range(MAXELEMENTS):
                txt += str(currentList.data[inx]) + " "
            txt += '] [ '
            currentList = currentList.next
        return txt


test = UnrolledLinkedList()
dummy = [i for i in range(0,10)]
for element in dummy:
    test.insert(element,element)
print(test.get(3))
test.insert(10,1)
test.insert(11,8)
print(test)
test.delete(1)
test.delete(2)
print(test)

