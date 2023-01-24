#!/usr/bin/python
# -*- coding: utf-8 -*-

#do dokończneia

import numpy as np
import mmh3

with open("lotr.txt", encoding='utf-8') as f:
    text = f.readlines()
f.close()

S = ' '.join(text).lower()

P = 0.001
n = 20
b = (-n) * np.log(P) / (np.log(2)**2)
b = b.astype('uint16')
k = b / n * np.log(2)
k = np.ceil(k).astype('uint16')


def check_if_occurance(source, hsubs):
    for hash_fun in range(k):
        inx = mmh3.hash(source, hash_fun) % b
        if not hsubs[inx]:
            return False
    return True

def RabingKarpSet(s, pattern, n):
    occur = 0
    false_positive_num = 0
    false_positive_el = []
    word_len = len(pattern[0])

    hsubs = [0] * n

    for hash_fun in range(k):
        for pattern_inx in range(len(pattern)):
            inx = mmh3.hash(pattern[pattern_inx], hash_fun) % n
            hsubs[inx] = True

    for m in range(len(s) - word_len):
        if check_if_occurance(s[m:m+word_len], hsubs):
            if s[m:m+word_len] in pattern:
                occur += 1
            else:
                false_positive_num += 1
    return occur, false_positive_num

patterns = ['gandalf', 'looking', 'blocked', 'comment', 'pouring', 'finally', 'hundred', 'hobbits', 'however', 'popular', 'nothing', 'enjoyed', 'stuffed', 'relaxed', 'himself', 'present', 'deliver', 'welcome', 'baggins', 'further']

occur, false_positive = RabingKarpSet(S, patterns, b)
print(occur, false_positive)



