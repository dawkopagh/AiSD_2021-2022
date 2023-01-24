#gotowe
#z przeprowadzonych testów wynika, że quadratic probing dla ograniczenia iteracji = rozmiarowi tablicy jest bardzo nieefektywny,
#modulo z kolejnych potęg się powtarza i przy niekorzystnych danych (a raczej w większości przypadków) nie wszystkie elementy zostaną poprawnie wprowadzone pomimo wolnego miejsca w tablicy
from copy import deepcopy

class Element():
    def __init__(self, key, value):
        self.key = key
        self.value = value

class HashTable:
    def __init__(self, size=5, c1=1, c2=0):
        self.tab = [None for i in range(size)]
        self.size = size
        self.c1 = c1
        self.c2 = c2

    def key2int(self, key):
        if isinstance(key, str):
            inx = 0
            for letter in key:
                inx += ord(letter)
        else:
            inx = deepcopy(key)
        return inx

    def modSize(self, inx):
        return inx % self.size

    def hash(self, key, c1, c2):
        key = self.key2int(key)
        inx = self.modSize(key)
        iter = 1
        possible_element = self.tab[(key + c1 * iter + c2 * iter ** 2)%self.size]
        if self.tab[inx] is None and possible_element is not None and self.key2int(possible_element.key) % self.size == self.key2int(key) % self.size:
            inx = self.modSize(key + c1 * iter + c2 * iter ** 2)
            iter += 1
        while self.tab[inx] is not None and self.tab[inx].key != key:
            inx = self.modSize(key + c1 * iter + c2 * iter ** 2)
            iter += 1
            if iter == self.size+1:
                break
            possible_element = self.tab[(key + c1 * iter + c2 * iter ** 2) % self.size]
            if self.tab[inx] is None and possible_element is not None and self.key2int(possible_element.key) % self.size == self.key2int(key) % self.size:
                if iter != self.size:
                    inx = self.modSize(key + c1 * iter + c2 * iter ** 2)
                    iter += 1
        if iter == self.size+1:
            return None
        return inx


    def insert(self, key, value):
        inx = self.hash(key, self.c1, self.c2)
        if inx is None:
            print("Brak miejsca")
        else:
            self.tab[inx] = Element(key, value)

    def search(self, key):
        inx = self.hash(key, self.c1, self.c2)
        if inx is None:
            return "Brak danej"
        elif self.tab[inx] is not None and self.tab[inx].key == key:
            return self.tab[inx].value

    def remove(self, key):
        inx = self.hash(key, self.c1, self.c2)
        if inx is None:
            print("Brak danej")
        elif self.tab[inx].key == key:
            self.tab[inx] = None

    def __str__(self):
        txt = '{'
        for inx in range(self.size):
            if self.tab[inx] is None:
                txt += str(None) + ", "
            else:
                txt += str(self.tab[inx].key) + ":" + str(self.tab[inx].value) + ", "
        txt = txt[:-2]
        txt += '}'
        return txt

def test1(size=13, c1=1, c2=0):

    test = HashTable(size, c1, c2)
    test.insert(1,"A")
    test.insert(2,"B")
    test.insert(3,"C")
    test.insert(4,"D")
    test.insert(5,"E")
    test.insert(18,"F")
    test.insert(31,"G")
    test.insert(8,"H")
    test.insert(9,"I")
    test.insert(10,"J")
    test.insert(11,"K")
    test.insert(12,"L")
    test.insert(13,"M")
    test.insert(14,"N")
    test.insert(15,"O")

    print(test)
    print(test.search(5))
    print(test.search(14))
    test.insert(5,"Z")
    print(test.search(5))
    print()
    test.remove(5)
    print(test)
    print(test.search(31))
    test.insert("test", "W")
    print(test)

def test2(size=13, c1=1, c2=0):

    test = HashTable(size, c1, c2)
    test.insert(13, "A")
    test.insert(26, "B")
    test.insert(39, "C")
    test.insert(52, "D")
    test.insert(65, "E")
    test.insert(78, "F")
    test.insert(91, "G")
    test.insert(104, "H")
    test.insert(117, "I")
    test.insert(130, "J")
    test.insert(143, "K")
    test.insert(156, "L")
    test.insert(169, "M")

    print(test)


def main():
    test1()
    test2()
    test2(c1=0,c2=1)
    test1(c1=0,c2=1)

main()