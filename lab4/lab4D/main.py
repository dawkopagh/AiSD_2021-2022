from random import random
from copy import deepcopy, copy

def randomLevel(p, maxLevel):
  lvl = 1
  while random() < p and lvl < maxLevel:
        lvl = lvl + 1
  return lvl

class Element:
    def __init__(self, key=None, value=None, levels=None):
        self.key = key
        self.value = value
        self.levels = levels
        self.next = [None] * levels

class SkipList:
    def __init__(self, maxLevel):
        self.head = Element(levels=maxLevel)
        self.maxLevel = maxLevel

    def insert(self, key, value):

        recorded_path = [None] * self.maxLevel
        current_pointer = self.head
        for inx in range(self.head.levels-1, -1, -1):
            while current_pointer.next[inx] is not None and current_pointer.next[inx].key < key:
                current_pointer = current_pointer.next[inx]
                if current_pointer.next[inx] is not None and current_pointer.next[inx].key == key:
                    current_pointer.next[inx].value = value
                    return None
            recorded_path[inx] = current_pointer

        Node = Element(key, value, randomLevel(0.5, self.maxLevel))

        for inx in range(Node.levels):
            if inx < self.maxLevel:
                Node.next[inx] = recorded_path[inx].next[inx]
                recorded_path[inx].next[inx] = Node
            else:
                self.head.next[inx] = Node


    def search(self, key):
        current_pointer = self.head
        for inx in range(self.head.levels-1, -1, -1):
            while current_pointer is not None:
               if current_pointer.next[inx] is not None and current_pointer.next[inx].key == key:
                   return current_pointer.next[inx].value
               elif current_pointer.next[inx] is not None and current_pointer.next[inx].key < key:
                    current_pointer = current_pointer.next[inx]
               else:
                   break
        return None

    def remove(self, key):
        recorded_path = [None] * self.maxLevel
        current_pointer = self.head
        nodeFound = False
        for inx in range(self.head.levels-1, -1, -1):
            while current_pointer.next[inx] is not None and current_pointer.next[inx].key < key:
                current_pointer = current_pointer.next[inx]
            if current_pointer.next[inx] is not None and current_pointer.next[inx].key == key:
                nodeFound=True

            recorded_path[inx] = current_pointer
        if not nodeFound:
            return None
        removed_node = current_pointer.next[0]
        for inx in range(len(removed_node.next)):
            if recorded_path[inx] is not None:
                recorded_path[inx].next[inx] = removed_node.next[inx]

    def displayList_(self):
        node = self.head.next[0]  # pierwszy element na poziomie 0
        keys = []                           # lista kluczy na tym poziomie
        while(node != None):
            keys.append(node.key)
            node = node.next[0]

        for lvl in range(self.maxLevel-1, -1, -1):
            print("{}: ".format(lvl), end=" ")
            node = self.head.next[lvl]
            idx = 0
            while(node != None):
                while node.key>keys[idx]:
                    print("  ", end=" ")
                    idx+=1
                idx+=1
                print("{:2d}".format(node.key), end=" ")
                node = node.next[lvl]
            print("")

def main():
    dummy = SkipList(4)
    test = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"]
    for inx in range(1,16):
        dummy.insert(inx,test[inx-1])
    dummy.displayList_()
    print(dummy.search(2))
    dummy.insert(2, "Z")
    print(dummy.search(2))
    dummy.remove(5)
    dummy.remove(6)
    dummy.remove(7)
    dummy.displayList_()
    dummy.insert(6, "W")
    dummy.displayList_()

    dummy = SkipList(4)
    test = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"]
    for inx in range(1,16):
        dummy.insert(len(test)-inx+1,test[len(test)-inx])
    dummy.displayList_()
    print(dummy.search(2))
    dummy.insert(2, "Z")
    print(dummy.search(2))
    dummy.remove(5)
    dummy.remove(6)
    dummy.remove(7)
    dummy.displayList_()
    dummy.insert(6, "W")
    dummy.displayList_()

main()