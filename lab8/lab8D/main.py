import random
import time
import copy
from typing import List

def Shell(list):
    table = copy.deepcopy(list)
    h = len(table)//2
    while h >= 1:
        for iter in range(h, len(list)):
            buffer = table[iter]
            j = iter
            while j >= h and table[j-h] > buffer:
                table[j] = table[j-h]
                j -= h
            table[j] = buffer
        h = h//2
    return table

def all_equal(list):
    value = list[0]
    for element in list:
        if element != value:
            return False
    return True


def median_3(a, b, c):
    return max(min(a,b),min(c,max(a,b)))

def median_5(a, b, c, d, e):
      f=max(min(a,b),min(c,d)) # usuwa najmniejsza z 4
      g=min(max(a,b),max(c,d)) # usuwa największą z 4
      return median_3(e,f,g)

def median(list):
    list_of_fives = [list[x:x + 5] for x in range(0, len(list), 5)]
    if len(list) == 1:
        return list[0]
    for cell_inx in range(len(list_of_fives)):
        list_of_fives[cell_inx] = median_of_cell(list_of_fives[cell_inx])
    list_of_fives = median(list_of_fives)
    return list_of_fives

def median_of_cell(list):
    if len(list) == 1:
        return list[0]
    elif len(list) == 2:
        return sum(list)/2
    elif len(list) == 3:
        return median_3(list[0], list[1], list[2])
    elif len(list) == 4:
        mid1 = max(min(list[0], list[1]), min(list[2], list[3]))
        mid2 = min(max(list[0], list[1]), max(list[2], list[3]))
        return (mid1+mid2)/2
    else:
        return median_5(list[0],list[1],list[2],list[3],list[4])

def median_sort(to_sort):
    if len(to_sort) <= 1 or all_equal(to_sort) :
        return to_sort
    smaller = []
    equal = []
    greater = []
    pivot = median(to_sort)
    for element in to_sort:
        if element > pivot:
            greater.append(element)
        elif element == pivot:
            equal.append(element)
        elif element < pivot:
            smaller.append(element)

    return median_sort(smaller) + median_sort(equal) + median_sort(greater)

def quicksort(to_sort):
    smaller = []
    equal = []
    greater = []
    if len(to_sort) <= 1:
        return to_sort
    pivot = to_sort[0]
    for element in to_sort:
        if element > pivot:
            greater.append(element)
        elif element == pivot:
            equal.append(element)
        elif element < pivot:
            smaller.append(element)

    return median_sort(smaller) + median_sort(equal) + median_sort(greater)

test_table = []
for iter in range(10001):
    test_table.append(int(random.random() * 100))

t_start = time.perf_counter()
Shell(test_table)
t_stop = time.perf_counter()
print("Czas obliczeń dla sortowania metodą Shella:", "{:.7f}".format(t_stop - t_start))

t_start = time.perf_counter()
median_sort(test_table)
t_stop = time.perf_counter()
print("Czas obliczeń dla sortowania metodą median:", "{:.7f}".format(t_stop - t_start))

t_start = time.perf_counter()
quicksort(test_table)
t_stop = time.perf_counter()
print("Czas obliczeń dla sortowania metodą klasycznego quicksort:", "{:.7f}".format(t_stop - t_start))


