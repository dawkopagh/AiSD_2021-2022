from copy import deepcopy

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
    def __init__(self):
        self.list = []
        self.size = 0

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
        self.list[0] = self.list[self.size-1]
        self.size -= 1
        current_inx = 0
        self.list.pop()

        while current_inx < self.size:
            first_comp = self.left(current_inx)
            second_comp = self.right(current_inx)
            if first_comp < self.size and second_comp < self.size and self.list[current_inx] < self.list[first_comp] and self.list[first_comp] > self.list[second_comp]:
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
        insert_inx = len(self.list)-1
        parent_inx = (insert_inx-1)//2
        self.size += 1

        while self.list[insert_inx] > self.list[parent_inx] and parent_inx >= 0:
            self.swap(insert_inx, parent_inx)
            buff = parent_inx
            parent_inx = (parent_inx-1)//2
            insert_inx = buff

    def left(self, inx):
        return 2*inx+1

    def right(self, inx):
        return 2*inx+2

    def parent(self, inx):
        return (inx-1)//2

    def print_tab(self):
        if not self.size:
            print('{}')
            return None
        print ('{', end=' ')
        for i in range(self.size-1):
            print(self.list[i], end = ', ')
        if self.list[self.size-1]: print(self.list[self.size-1] , end = ' ')
        print( '}')

    def print_tree(self, idx, lvl):
        if idx<self.size:
            self.print_tree(self.right(idx), lvl+1)
            print(2*lvl*'  ', self.list[idx] if self.list[idx] else None)
            self.print_tree(self.left(idx), lvl+1)


dummy = Queue()

a = [4, 7, 6, 7, 5, 2, 2, 1]
txt = "ALGORYTM"

for inx in range(len(a)):
    dat = qElement(a[inx],txt[inx])
    dummy.enqueue(dat)

dummy.print_tree(0, 0)
dummy.print_tab()
print(dummy.dequeue())
print(dummy.peek())
dummy.print_tab()
dummy.print_tree(0,0)
for inx in range(dummy.size):
    print(dummy.dequeue())
dummy.print_tab()