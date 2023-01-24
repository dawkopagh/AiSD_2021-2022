#gotowe
from copy import deepcopy

def realloc(tab,size):
    oldSize = len(tab)
    return [tab[i] if i < oldSize else None for i in range(size)]

class queue:
    def __init__(self):
        self.tab = [None for i in range(5)]
        self.writeINX = 0
        self.readINX = 0
        self.size = 5

    def is_empty(self):
        if self.writeINX == self.readINX:
            return True
        else:
            return False

    def peek(self):
        return self.tab[self.readINX]


    def dequeue(self):
        if self.is_empty():
            return None
        else:
            readBuffer = self.readINX
            if self.readINX + 1 == self.size:
                self.readINX = 0
            else:
                self.readINX += 1
            return self.tab[readBuffer]

    def enqueue(self, data):
        if (self.writeINX + 1) % self.size == self.readINX % self.size:
            self.tab = realloc(self.tab, self.size*2)
            self.tab[self.size:] = self.tab[:self.size]
            self.tab[:self.size] = [None] * self.size       #właściwie to ta operacja jest zbędna, gdyż nie wpływa ona na stan kolejki, ale dodałem
            self.readINX = self.size+self.readINX                      #ją żeby zwiększyć czytelność przy wypisywaniu listy i jeśli dosłownie rozumieć polecenie, to
            self.size = self.size*2                         #zamazujemy dane które zostały przesunięte na koniec listy.
            self.writeINX = 0
            self.tab[self.writeINX] = data
            self.writeINX += 1
        elif self.writeINX + 1 == self.size:
            self.tab[self.writeINX] = data
            self.writeINX = 0
        else:
            self.tab[self.writeINX] = data
            self.writeINX += 1

    def print_list(self):
        txt = ''
        txt += '[' + str(self.tab[0]) + ", "
        for inx in range(self.size-2):
            txt += str(self.tab[inx+1]) + ", "
        txt += str(self.tab[self.size-1]) + "]"
        return txt

    def print_queue(self):
        txt = '['
        dummy_read_inx = deepcopy(self.readINX) + 1
        dummy_write_inx = deepcopy(self.writeINX)

        if not self.is_empty():
            txt += str(self.tab[self.readINX]) + ', '
            while (dummy_write_inx - 1) % self.size != dummy_read_inx % self.size:
                txt += str(self.tab[dummy_read_inx % self.size]) + ", "
                dummy_read_inx += 1
            txt += str(self.tab[dummy_read_inx % self.size])
        txt += "]"
        return txt

def main():
    test = queue()
    tab = [1,2,3,4]
    for element in tab:
        test.enqueue(element)
    print(test.dequeue())
    print(test.dequeue())
    print(test.dequeue())
    print(test.peek())
    print(test.print_queue())
    print(test.print_list())
    tab = [5,6,7,8]
    for element in tab:
        test.enqueue(element)
    print(test.print_list())
    while not test.is_empty():
        print(test.dequeue())
    print(test.print_queue())

main()