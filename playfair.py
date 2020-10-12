#/usr/local/bin/python3
import numpy as np
import sys

if len(sys.argv) < 2:
   print("usage: encode/decode ciphertext/plaintext keytext")
   sys.exit()

job = sys.argv[1]
if job == "encode":
    direction = 1
else:
    direction = -1

text = sys.argv[2].upper()
for i in range(3, len(sys.argv) - 1):
    text += sys.argv[i].upper()

keytext = sys.argv[-1]
if len(keytext) != 25:
    print("key must be 25 letters")
    sys.exit()

key = np.empty((5,5), dtype=object)
ind = 0
for i in range(5):
    for j in range(5):
        key[i][j] = keytext[ind]
        ind += 1

# remove whitespace, remove non-alpha characters, add x, j = i, add z
def prep(s):
    # make uppercase, remove non-alpha
    s = s.upper()
    new = ""
    for i in s:
        if i.isalpha():
            new += i
    s = new
    # replace j with i
    new = ""
    for i in s:
        if i == "J":
            new += "I"
        else:
            new += i
    s = new
    # adding x between double letters, adding z (or x if already ends in z) if odd
    # go until done
    new = ""
    shift = 0
    for i in range(len(s)):
        if (i + shift) % 2 == 1 and s[i] == s[i - 1]:
            new += "X"
            shift += 1
        new += s[i]
    s = new
    if len(s) % 2 == 1:
        if s[-1] != "Z":
            s = s + "Z"
        else:
            s = s + "X"
    return s
#print(prep("z"))

# encode/decode two letters in the same column
def vertical(pair):
    new = ""
    for i in pair:
        coord = np.where(key == i)
        new += key[coord[0][0]][(coord[1][0] + direction) % 5]
    return new

# encode/decode two letters in the same row
def horizontal(pair):
    new = ""
    for i in pair:
        coord = np.where(key == i)
        new += key[(coord[0][0] + direction) % 5][coord[1][0]]
    return new

# encode/decode two letters in different column and different row
def regular(pair):
    new = ""
    coord0 = np.where(key == pair[0])
    coord1 = np.where(key == pair[1])
    new += key[coord0[0][0]][coord1[1][0]]
    new += key[coord1[0][0]][coord0[1][0]]
    return new    

# decide which encode/decode function to use, return encoded/decoded pair
def doPair(pair):
    coord0 = np.where(key == pair[0])
    coord1 = np.where(key == pair[1])
    if coord0[0][0] == coord1[0][0]:
        return horizontal(pair)
    if coord0[1][0] == coord1[1][0]:
        return vertical(pair)
    return regular(pair)

# encodes/decodes string s
def encode(s):
    s = prep(s)
    new = ""
    for i in range(int(len(s) / 2)):
        new += doPair(s[2*i: 2*i + 2])
    return new

print(encode(text))