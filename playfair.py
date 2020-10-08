#/usr/local/bin/python3
import numpy as np
import sys

if len(sys.argv) < 2:
   print("usage: encode/decode ciphertext/plaintext keytext")
   sys.exit()
#args = sys.argv[1].split()
#print(args)
job = sys.argv[1]
if job == "encode":
    direction = 1
else:
    direction = -1
text = sys.argv[2].upper()
keytext = sys.argv[3]
#print(job + " " + text + " " + keytext)

key = np.empty((5,5), dtype=object)
ind = 0
for i in range(5):
    for j in range(5):
        key[i][j] = keytext[ind]
        ind += 1
#print(key)

# remove whitespace, add x, j = i, add z
def condition(s):
    s = s.upper()
    new = ""
    for i in s:
        if i.isalpha():
            new += i
    s = new
    new = ""
    for i in s:
        if i == "J":
            new += "I"
        else:
            new += i
    s = new
    new = ""
    shift = 0
    for i in range(len(s)):
        if (i + shift) % 2 == 1 and s[i] == s[i - 1]:
            new += "X"
            shift += 1
        new += s[i]
    if len(s) % 2 == 1:
        s = s + "Z"
    return new

# encode letter pairs
def vertical(pair):
    new = ""
    for i in pair:
        coord = np.where(key == i)
        new += key[coord[0][0]][(coord[1][0] + direction) % 5]
    return new

def horizontal(pair):
    new = ""
    for i in pair:
        coord = np.where(key == i)
        new += key[(coord[0][0] + direction) % 5][coord[1][0]]
    return new
    
def regular(pair):
    new = ""
    coord0 = np.where(key == pair[0])
    coord1 = np.where(key == pair[1])
    new += key[coord0[0][0]][coord1[1][0]]
    new += key[coord1[0][0]][coord0[1][0]]
    return new    

def doPair(pair):
    coord0 = np.where(key == pair[0])
    coord1 = np.where(key == pair[1])
    if coord0[0][0] == coord1[0][0]:
        return horizontal(pair)
    if coord0[1][0] == coord1[1][0]:
        return vertical(pair)
    return regular(pair)

# s is uppercase, no spaces
def encode(s):
    s = condition(s)
    new = ""
    for i in range(int(len(s) / 2)):
        new += doPair(s[2*i: 2*i + 2])
    return new

print(encode(text))