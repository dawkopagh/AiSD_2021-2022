import numpy as np

def string_compare_recursive(p, t, i, j):
    if i == 0:
        return len(t[:j])
    if j == 0:
        return len(p[:i])
    zam = string_compare_recursive(p,t,i-1,j-1) + (p[i-1] != t[j-1])
    wst = string_compare_recursive(p,t,i,j-1) + 1
    usun = string_compare_recursive(p,t,i-1,j) + 1

    return min(zam,wst,usun)

def string_compare_PD(p, t, i, j):
    D = np.zeros((i,j))
    for inx in range(i):
        D[inx,0] = inx
    for inx in range(j):
        D[0,inx] = inx

    parent = np.chararray((i,j))
    parent.fill('X')
    parent[0,1:j] = 'I'
    parent[1:i,0] = 'D'

    for row in range(1,i):
        for col in range(1,j):
            zam = D[row-1,col-1] + (p[row] != t[col])
            wst = D[row,col-1] + 1
            usun = D[row-1,col] + 1
            D[row, col] += min(zam,wst,usun)
            if zam == min(zam,wst,usun) and p[row] != t[col]:
                parent[row,col] = 'S'
            elif p[row] == t[col]:
                parent[row,col]  = 'M'
            elif wst == min(zam,wst,usun):
                parent[row,col] = 'I'
            elif usun == min(zam,wst,usun):
                parent[row,col] = 'D'
    return D, parent

def reproduction(lst):
    i, j = np.shape(lst)
    i -= 1
    j -= 1

    result = ''

    while i >= 0 and j >= 0:
        if lst[i,j] == b'S':
            result += 'S' #zmiana znaków
            i -= 1
            j -= 1
        elif lst[i,j] == b'M':
            result += 'M' #zgodne
            i -= 1
            j -= 1
        elif lst[i,j] == b'D':
            result += 'D' #usunięcie znaku
            i -= 1
        elif lst[i,j] == b'I':
            result += 'I' #wstawienie znaku
            j -= 1
        elif lst[i,j] == b'X':
            j -= 1
    return result[::-1]

def goal_cell(p, t, i, j, D):
    i = len(p) - 1
    j = 0
    for k in range(len(t)):
        if D[i,k] < D[i, j]:
            j = k
    return j

def string_fit(p, t, i, j):
    D = np.zeros((i,j))
    for inx in range(i):
        D[inx,0] = inx
    for inx in range(j):
        D[0,inx] = 0

    parent = np.chararray((i,j))
    parent.fill('X')
    parent[1:i,0] = 'D'

    for row in range(1,i):
        for col in range(1,j):
            zam = D[row-1,col-1] + (p[row] != t[col])
            wst = D[row,col-1] + 1
            usun = D[row-1,col] + 1
            D[row, col] += min(zam,wst,usun)
            if zam == min(zam,wst,usun) and p[row] != t[col]:
                parent[row,col] = 'S'
            elif p[row] == t[col]:
                parent[row,col]  = 'M'
            elif wst == min(zam,wst,usun):
                parent[row,col] = 'I'
            elif usun == min(zam,wst,usun):
                parent[row,col] = 'D'

    inx = goal_cell(p, t, i, j, D)
    return inx - len(p) + 1

def obtain_text(p, t, reproduced):
    res = ''
    I_cnt = 0
    D_cnt = 0
    for inx in range(len(reproduced)):
        if reproduced[inx] == 'M':
            res += t[inx-I_cnt+D_cnt]
        if reproduced[inx] == 'I':
            D_cnt = 1
        if reproduced[inx] == 'D':
            I_cnt += 1
    return res

def longest_sequence(p, t, i, j):
    D = np.zeros((i,j))
    for inx in range(i):
        D[inx,0] = inx
    for inx in range(j):
        D[0,inx] = inx

    parent = np.chararray((i,j))
    parent.fill('X')
    parent[0,1:j] = 'I'
    parent[1:i,0] = 'D'

    for row in range(1,i):
        for col in range(1,j):
            th = 0
            if p[row] != t[col]:
                th = 999
            zam = D[row-1,col-1] + th
            wst = D[row,col-1] + 1
            usun = D[row-1,col] + 1
            D[row, col] += min(zam,wst,usun)
            if zam == min(zam,wst,usun) and p[row] != t[col]:
                parent[row,col] = 'S'
            elif p[row] == t[col]:
                parent[row,col]  = 'M'
            elif wst == min(zam,wst,usun):
                parent[row,col] = 'I'
            elif usun == min(zam,wst,usun):
                parent[row,col] = 'D'
    res = obtain_text(p, t, reproduction(parent))
    return res

#zad a

P = ' kot'
T = ' pies'
print(string_compare_recursive(P, T, len(P), len(T)))
#zad b
P = ' biały autobus'
T = ' czarny autokar'
a, b = string_compare_PD(P, T, len(P), len(T))
print(a[-1,-1])

#zad c
P = ' thou shalt not'
T = ' you should not'
a, b = string_compare_PD(P,T,len(P),len(T))
res  = reproduction(b)
print(res)

# zad d
P = 'ban'
T = 'mokeyssbanana'
print(string_fit(P, T, len(P), len(T)))

P = 'bin'
print(string_fit(P, T, len(P), len(T)))

#zad e
P = ' democrat'
T = ' republican'

print(longest_sequence(P, T, len(P), len(T)))

#zad f
P = ' 123456789'
T = ' 243517698'

print(longest_sequence(P, T, len(P), len(T)))