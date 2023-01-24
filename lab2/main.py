from copy import copy

class ListElements:
    def __init__(self, element=None):
        self.data = element
        self.next = None

class LinkedList:
    def __init__(self) -> None:
        self.head = None
        self.elements = ListElements()

    def destroy(self) -> None:
        self.head = None
        self.elements = None

    def add(self, other) -> None:
        if not self.head:
            self.head = other
            self.elements.data = other
        else:
            self.elements.next = copy(self.elements)
            self.head = other
            self.elements.data = other

    def remove(self) -> None:
        self.head = self.elements.next.data
        self.elements = self.elements.next


    def is_empty(self) -> bool:
        if not self.head:
            return True
        else:
            return False

    def length(self) -> int:
        if not self.head:
            return 0
        counter = 1
        iterator = self.elements
        while iterator.next:
            iterator = iterator.next
            counter += 1
        return counter

    def get(self):
        return self.head

    def __str__(self) -> str:
        text = ''
        iterator = self.elements
        if self.head is None:
            return "list is empty."
        while True:
            text += str(iterator.data) + '\n'
            iterator = iterator.next
            if not iterator:
                return text

    def __add__(self, other):
        if self.is_empty():
            self.head = other
            self.elements.data = other
            return self
        iterator = self.elements
        while iterator.next:
            iterator = iterator.next
        if iterator.next == None:
            iterator.next = ListElements(other)
        return self

    def delete(self) -> None:
        iterator = self.elements
        prev_iter = 0
        while iterator.next:
            prev_iter = iterator
            iterator = iterator.next
        if iterator.next == None:
            prev_iter.next = None
        return self

    def take(self, n):
        if n > self.length():
            n = self.length()

        NewLinkedList = LinkedList()
        iterator = self.elements
        for inx in range(0,n):
            NewLinkedList += iterator.data
            iterator = iterator.next
        return NewLinkedList

    def drop(self, n):
        if n > self.length():
            return LinkedList()
        else:
            NewLinkedList = LinkedList()
            iterator = self.elements
            counter = 1
            while iterator.next:
                iterator = iterator.next
                if counter >= n:
                    NewLinkedList += iterator.data
                counter += 1
            return NewLinkedList

def main():

    dummy = [('AGH', 'Kraków', 1919),
    ('UJ', 'Kraków', 1364),
    ('PW', 'Warszawa', 1915),
    ('UW', 'Warszawa', 1915),
    ('UP', 'Poznań', 1919),
    ('PG', 'Gdańsk', 1945)]

    list = LinkedList()
    for element in dummy:
        list += element

    print("Lista po dodaniu wszystkich elementów: ")
    print(list)

    print("Lista po dodaniu elementu na początek: ")
    list.add("TEST")
    print(list)

    print("Lista po usunięciu elementu z początku: ")
    list.remove()
    print(list)

    print("Sprawdzenie czy lista jest pusta: ")
    print(list.is_empty(), "\n")

    print("Sprawdzenie listy pustej: ")
    list2 = LinkedList()
    print(list2.is_empty(), "\n")

    print("Sprawdzenie długości listy, oczekiwane 6: ")
    print(list.length(), "\n")

    print("Zwrócenie pierwszego elementu: ")
    print(list.get(), "\n")

    print("Lista po dodaniu elementu na koniec: ")
    list += "TEST"
    print(list)

    print("Lista po usunięciu elementu z końca: ")
    list.delete()
    print(list)

    print("Pierwsze 3 elementy listy: ")
    print(list.take(3))

    print("Ostatnie 3 elementy listy: ")
    print(list.drop(3))

    print("Destruktor: ")
    list.destroy()
    print(list)

main()