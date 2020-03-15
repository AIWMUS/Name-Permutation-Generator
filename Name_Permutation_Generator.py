# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 19:51:21 2020

@author: MazyCrazy
"""

import os

CNT = 2
P = [37, 53]
M = [1000000007, 1073676287]
LIMIT = int(1e9)

"""
print("а", ord("а"))
print("я", ord("я"))
print("А", ord("А"))
print("Я", ord("Я"))
print("ё", ord("ё"))
print("Ё", ord("Ё"))
print("-", ord("-"))
"""

abs_file_path = os.path.dirname(os.path.realpath(__file__))
print("Absolute file path (dir): " + abs_file_path)
print("Step: Precalculations...")

p = []
for j in range(CNT):
    p.append(1)
ppow = []
for i in range(2000):
    ppow.append(p.copy())
    for j in range(CNT):
        p[j] *= P[j]
        p[j] %= M[j]

def hash_string(s):
    new_s = s.lower()
    hash_val = []
    for j in range(CNT):
        hash_val.append(0)
    for c in new_s:
        for j in range(CNT):
            hash_val[j] = (hash_val[j] + ppow[ord(c)][j]) % M[j]
    return hash_val

name = input("Input name: ")
name = "".join(name.split(" "))
name_hash = hash_string(name)

print("Step: Reading words...")

words_file = open(abs_file_path + "/russian.dic", "r")
words_list = words_file.readlines()
words_list = [x.strip() for x in words_list]

print("Step: Processing words...")

words_hashes_list = []
words_hashes_dict = dict()
words_cnt = min(LIMIT, len(words_list))
mx = 0
for i in range(words_cnt):
    s = words_list[i]
    hash_val = hash_string(s)
    words_hashes_list.append(hash_val)
    if words_hashes_dict.get(hash_val[0]) is None:
        words_hashes_dict[hash_val[0]] = []
    words_hashes_dict[hash_val[0]].append(i)
    mx = max(mx, len(words_hashes_dict[hash_val[0]]))

print("Max count of Collisions: " + str(mx))
print("Average count of Collisions: " + \
      str(words_cnt / len(words_hashes_dict)))
print("Step: Calculating Result...:")
print()

for i in range(words_cnt):
    s1 = words_list[i]
    s1_hash = words_hashes_list[i]
    if len(s1) >= len(name):
        continue
    s2_hash = []
    for j in range(CNT):
        s2_hash.append((name_hash[j] - s1_hash[j] + M[j]) % M[j])
    s2_is = words_hashes_dict.get(s2_hash[0])
    if s2_is is None:
        continue
    for s2_i in s2_is:
        if words_hashes_list[s2_i] == s2_hash:
            print(s1, words_list[s2_i])

print()
print("Step: End!")
