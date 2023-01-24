# <Dawid> <Kopeć>, <405602>

from typing import List
import copy
import math


def quicksort(to_sort: List[int]) -> List[int]:
    def quicksort_inplace(to_sort: List[int], start: int, stop: int, copied = False) -> List[int]:
        if not copied:                              #Sprawdzamy czy lista przekazana jako argument
            sorted_list = copy.deepcopy(to_sort)    #została już skopiowana - ta powinna zostać niezmieniona
            copied = True                           #będzie to niezbędne przy wywołaniach rekurencyjnych.
        else:
            sorted_list = to_sort
        i = start
        j = stop
        middle_index = math.floor((i + j) / 2)  #Pivot - element rozstrzygający wbieramy znajdując
        pivot = sorted_list[middle_index]       #element leżący na środku zakresu tablicy.

        while i < j:
            while sorted_list[i] < pivot:
                i += 1
            while sorted_list[j] > pivot:
                j -= 1

            if i <= j:
                (sorted_list[i], sorted_list[j]) = (sorted_list[j], sorted_list[i])
                i += 1
                j -= 1

        if start < j:
            quicksort_inplace(sorted_list, start, j, copied)
        if i < stop:
            quicksort_inplace(sorted_list, i, stop, copied)
        return sorted_list
    return quicksort_inplace(to_sort,0,(len(to_sort)-1))



def bubblesort(list_not_sorted: List[int]) -> (List[int], int):
    sorted_list = copy.deepcopy(list_not_sorted)
    list_len = len(list_not_sorted)
    comparison_num = 0

    for it in range(0, list_len):
        swap_occured = False                 #flaga zamiany.
        for elem in range(0, list_len - 1):
            comparison_num += 1
            if sorted_list[elem] > sorted_list[elem + 1]:
                (sorted_list[elem], sorted_list[elem + 1]) = (sorted_list[elem + 1], sorted_list[elem])
                swap_occured = True
        list_len -= 1
        if not swap_occured:
            return sorted_list, comparison_num
