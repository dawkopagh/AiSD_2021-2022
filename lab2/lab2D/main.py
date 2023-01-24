from copy import deepcopy

class LinkedList:
    def __init__(self) -> None:
        self.head = None
        self.next = None

def nil():
    return LinkedList()

def cons(el, list: LinkedList):
    result = nil()
    result.head = el
    result.next = deepcopy(list)
    return result

def first(list: LinkedList):
    return deepcopy(list.head)

def rest(list: LinkedList):
    return deepcopy(list.next)

def create():
    return nil()

def destroy(list: LinkedList) -> None:
    list = nil()

def is_empty(list: LinkedList) -> bool:
    if not first(list) or first(list) is None:
        return True
    else:
        return False

def add_end(el, list: LinkedList):
    if first(list) is None:
        return cons(el, list)
    else:
        first_el = first(list)
        rest_lst = rest(list)
        recreated_lst = add_end(el, rest_lst)
        return cons(first_el, recreated_lst)

def remove(list: LinkedList):
    result = nil()
    result = cons(first(rest(list)), result)
    result.next = rest(rest(list))
    return result

def length(list: LinkedList, counter = 0):
    if is_empty(list):
        return counter
    if rest(list) is None:
        return counter+1
    else:
        counter += 1
        if rest(list) is not None:
            counter = length(rest(list), counter)
    return counter

def print_out(list: LinkedList):
    if not is_empty(list):
        print(first(list))
        if rest(list) is not None:
            print_out(rest(list))

def delete_last(list: LinkedList):         #tą funkcję można zaimplementować w sposób znacznie prostszy
    if first(rest(list)) is None:          # po prostu wywołujemy funkcję take dla n = dlugość listy - 1
        return False
    else:
        first_el = first(list)
        rest_lst = rest(list)
        lst = delete_last(rest_lst)
        if not lst:
            return cons(first_el,nil())
        return cons(first_el, lst)

def take(n, list: LinkedList, counter=1):
    if n > length(list):
        return list
    if n == counter:
        return cons(first(list), nil())
    else:
        res = take(n, rest(list), counter+1)
        return cons(first(list),res)

def drop(n, list: LinkedList):
    if length(list) < n:
        return nil()
    if length(list) == n:
        return list
    if length(list) == 1:
        return list
    else:
        res = drop(n, rest(list))
        if length(res) != n:
            res = cons(first(list), res)
        if length(res) == n:
            return res



dummy = [('AGH', 'Kraków', 1919),
('UJ', 'Kraków', 1364),
('PW', 'Warszawa', 1915),
('UW', 'Warszawa', 1915),
('UP', 'Poznań', 1919),
('PG', 'Gdańsk', 1945)]

print("Stworzenie i dodanie elementów do listy:")
test = create()
for element in dummy:
    test = add_end(element,test)
print_out(test)
print()

print("Dodanie elementu na początek")
test = cons("TEST",test)
print_out(test)
print()

print("Usunięcie pierwszego elementu w liście:")
test = remove(test)
print_out(test)
print()

print("Wywołanie funkcji is_empty dla kolejno listy z elementami i pustej:")
print(is_empty(test))
print(is_empty(nil()))
print()

print("Wywołanie funkcji length, oczekiwana odpowiedź - 6:")
print(length(test))
print()

print("Funkcja zwracająca pierwszy element:")
print(first(test))
print()

print("Funkcja dodająca element na koniec listy:")
test = add_end("TEST",test)
print_out(test)
print()

print("Funkcja usuwająca ostatni element z listy:")
test = delete_last(test)
print_out(test)
print()

print("Funkcja tworząca nową listę z n (n=3) pierwszych elementów listy:")
taken = take(3,test)
print_out(taken)
print()

print("Funkcja tworząca nową listę z n (n=3) ostatnich elementów listy:")
dropped = drop(3, test)
print_out(dropped)