# gotowe

from copy import deepcopy
import random
import time


class qElement:
    def __init__(self, prior, data):
        self.data = data
        self.prior = prior

    def __str__(self):
        return str(self.prior) + ":" + str(self.data)

    def __lt__(self, other):
        res = self.prior < other.prior
        return res

    def __gt__(self, other):
        return self.prior > other.prior


class Queue:
    def __init__(self, toSort = None, printHeapFlag = True):
        self.list = []
        self.size = 0
        if toSort:
            heapify(toSort, printHeapFlag)


    def swap(self, insert_inx, parent_inx):
        buff = deepcopy(self.list[insert_inx])
        self.list[insert_inx] = self.list[parent_inx]
        self.list[parent_inx] = buff

    def is_empty(self):
        if len(self.list):
            return False
        else:
            return True

    def peek(self):
        return self.list[0]

    def dequeue(self):
        if self.is_empty():
            return None

        res = deepcopy(self.list[0])
        self.list[0] = self.list[self.size - 1]
        self.list[self.size - 1] = res
        self.size -= 1
        current_inx = 0

        while current_inx < self.size:
            first_comp = self.left(current_inx)
            second_comp = self.right(current_inx)
            if first_comp < self.size and second_comp < self.size and self.list[current_inx] < self.list[first_comp] and \
                    self.list[first_comp] > self.list[second_comp]:
                self.swap(current_inx, first_comp)
                current_inx = first_comp
            elif second_comp < self.size and self.list[current_inx] < self.list[second_comp]:
                self.swap(current_inx, second_comp)
                current_inx = second_comp
            else:
                return res
        return res

    def enqueue(self, data):
        self.list.append(data)
        insert_inx = len(self.list) - 1
        parent_inx = (insert_inx - 1) // 2
        self.size += 1

        while self.list[insert_inx] > self.list[parent_inx] and parent_inx >= 0:
            self.swap(insert_inx, parent_inx)
            buff = parent_inx
            parent_inx = (parent_inx - 1) // 2
            insert_inx = buff

    def left(self, inx):
        return 2 * inx + 1

    def right(self, inx):
        return 2 * inx + 2

    def parent(self, inx):
        return (inx - 1) // 2

    def size(self):
         return self.size()

    def print_tab(self):
        if not len(self.list):
            print('{}')
            return None
        print('{', end=' ')
        for i in range(len(self.list) - 1):
            print(self.list[i], end=', ')
        if self.list[self.size - 1]: print(self.list[self.size - 1], end=' ')
        print('}')

    def print_tree(self, idx, lvl):
        if idx < self.size:
            self.print_tree(self.right(idx), lvl + 1)
            print(2 * lvl * '  ', self.list[idx] if self.list[idx] else None)
            self.print_tree(self.left(idx), lvl + 1)

def heapify(toSort, printHeapFlag):
    heap = Queue()
    for element in toSort:
        heap.enqueue(element)
    if printHeapFlag:
        heap.print_tab()
        heap.print_tree(0, 0)
    for inx in range(heap.size):
        heap.dequeue()
    if printHeapFlag:
        heap.print_tab()


class Selement:
    def __init__(self, priority, value):
        self.priority = priority
        self.value = value

    def __lt__(self, other):
        return self.priority < other.priority

    def __gt__(self, other):
        return self.priority > other.priority

class Selection:
    def __init__(self):
        self.list = []

    def insert(self, element):
        self.list.append(element)

    def swap(self, inx1, inx2):
        self.list[inx1], self.list[inx2] = self.list[inx2], self.list[inx1]

    def shift(self):
        pass

    def min_inx(self, index):
        min = index
        for inx in range(index, len(self.list)):
            if self.list[inx] < self.list[min]:
                min = inx
        return min

    def print_table(self):
        print(self.list)

def selection_sort_swap(list):
    for inx in range(len(list.list)-1):
        m = list.min_inx(inx)
        list.swap(inx, m)

def selection_sort_shift(list): #nie jestem do końca pewny czy o taką implementację chodziło, gdyż nie znalazłem wyjaśnienia w materiałach z wykładu
    for inx in range(len(list.list)-1):
        m = inx
        minim = deepcopy(m)
        for element in range(inx, len(list.list)):
            if list.list[element] < list.list[m]:
                m = element
        list.swap(m, minim)


def testHeap():

    test_table = [(5,'A'), (5,'B'), (7,'C'), (2,'D'), (5,'E'), (1,'F'), (7,'G'), (5,'H'), (1,'I'), (2,'J')]
    Queue(test_table)

    test_table2 = []
    for iter in range(10001):
        test_table2.append(int(random.random()*100))

    t_start = time.perf_counter()
    Queue(test_table2, False)
    t_stop = time.perf_counter()
    print("Czas obliczeń dla sortowania przez kopcowanie:", "{:.7f}".format(t_stop - t_start))

def testSelectionSwap():
    test_table = [(5,'A'), (5,'B'), (7,'C'), (2,'D'), (5,'E'), (1,'F'), (7,'G'), (5,'H'), (1,'I'), (2,'J')]
    selection_table = Selection()
    for element in test_table:
        selection_table.insert(element)

    selection_sort_swap(selection_table)
    selection_table.print_table()

    test_table2 = Selection()
    for iter in range(10001):
        test_table2.insert(int(random.random() * 100))
    t_start = time.perf_counter()
    selection_sort_swap(test_table2)
    t_stop = time.perf_counter()
    print("Czas obliczeń dla sortowania przez wybieranie (Swap):", "{:.7f}".format(t_stop - t_start))

def testSelectionShift():
    test_table = [(5,'A'), (5,'B'), (7,'C'), (2,'D'), (5,'E'), (1,'F'), (7,'G'), (5,'H'), (1,'I'), (2,'J')]
    selection_table = Selection()
    for element in test_table:
        selection_table.insert(element)

    selection_sort_shift(selection_table)
    selection_table.print_table()

    test_table2 = Selection()
    for iter in range(10001):
        test_table2.insert(int(random.random() * 100))
    t_start = time.perf_counter()
    selection_sort_shift(test_table2)
    t_stop = time.perf_counter()
    print("Czas obliczeń dla sortowania przez wybieranie (Shift):", "{:.7f}".format(t_stop - t_start))


def main():
    testHeap()
    testSelectionSwap()
    testSelectionShift()

main()