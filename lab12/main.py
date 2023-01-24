import time

#gotowe

# Najszybsza metodą jest metoda Knutha-Morrisa-Pratta, wykonuje one także znacznie mniej porównań niż wcześniejsze metody.
# Usprawnienie metody Rabina-Karpa poprzez zaimplementowanie rolling-hasha skróca czas obliczeń ponad dwuktornie.
# Metoda naiwna mimo swojej prostoty nie odbiega od bardziej skomplikowanych metod czasem obliczeń. Jedynie ilość porównań jest spora (len(s)).

with open("lotr.txt", encoding='utf-8') as f:
    text = f.readlines()
f.close()

S = ' '.join(text).lower()

d = 256
q = 101  # liczba pierwsza

def hash(word, N):
    hw = 0
    for i in range(N):  # N - to długość wzorca
        hw = (hw*d + ord(word[i])) % q  # dla d będącego potęgą 2 można mnożenie zastąpić shiftem uzyskując pewne przyspieszenie obliczeń
    return hw

def naive(s, w):
    m = 0
    i = 0
    start_indices = []
    num_of_comparisons = 0
    while m < len(s):
        num_of_comparisons += 1
        if s[m:len(w)+m] == w:
            start_indices.append(m)
        m += 1

    return start_indices, num_of_comparisons

def RK(s, w):
    hW = hash(w, len(w))
    i = 0
    start_indices = []
    num_of_comparisons = 0
    num_of_collisions = 0

    for m in range(len(s) - len(w)+1):
        hS = hash(s[m:m + len(w)], len(w))
        num_of_comparisons += 1
        if hS == hW:
            if s[m:m + len(w)] == w:
                start_indices.append(m)
            else:
                num_of_collisions += 1

    return start_indices, num_of_comparisons, num_of_collisions

def RK_rolling_hash(s, w):
    hW = hash(w, len(w))
    start_indices = []
    num_of_comparisons = 0
    num_of_collisions = 0
    hS = hash(s[0:len(w)], len(w))


    h = 1
    for i in range(len(w) - 1):  # N - jak wyżej - długość wzorca
        h = (h * d) % q

    for m in range(len(s) - len(w)+1):

        num_of_comparisons += 1
        if hS == hW:
            if s[m:m + len(w)] == w:
                start_indices.append(m)
            else:
                num_of_collisions += 1
        if m < len(s)-len(w):
            hS = (d * (hS - ord(s[m]) * h) + ord(s[m+len(w)])) % q

    return start_indices, num_of_comparisons, num_of_collisions

def KMP_table(w):

    pos = 1
    cnd = 0
    T = [0] * (len(w)+1)

    T[0] = -1

    while pos < len(w):
        if w[pos] == w[cnd]:
            T[pos] = T[cnd]
        else:
            T[pos] = cnd
            while cnd >= 0 and w[pos] != w[cnd]:
                cnd = T[cnd]
        pos += 1
        cnd += 1
    T[pos] = cnd

    return T

def KMP(s, w):
    m = 0
    i = 0
    num_of_comparisons = 0
    start_indices = []
    T = KMP_table(w)

    while m < len(s):
        if w[i] == s[m]:
            m += 1
            i += 1
            num_of_comparisons += 1
            if i == len(w):
                start_indices.append(m - i)
                i = T[i]
        else:
            i = T[i]
            if i < 0:
                m += 1
                i += 1
    return start_indices, num_of_comparisons


# t_start = time.perf_counter()
ind, num = naive(S, "time.") #testowana metoda
print(len(ind), end=';')
print(num)
# t_stop = time.perf_counter()
# print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start))


# t_start = time.perf_counter()
# ind, num_comp, num_col = RK(S, "time.")   #testowana metoda
# print(len(ind), end=';')
# print(num_comp, end=';')
# print(num_col)
# t_stop = time.perf_counter()
# print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start))

# t_start = time.perf_counter()
ind, num_comp, num_col = RK_rolling_hash(S, "time.")   #testowana metoda
print(len(ind), end=';')
print(num_comp, end=';')
print(num_col)
# t_stop = time.perf_counter()
# print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start))

# t_start = time.perf_counter()
ind, num = KMP(S, "time.")   #testowana metoda
print(len(ind), end=';')
print(num)
# t_stop = time.perf_counter()
# print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start))
print(len(S))


