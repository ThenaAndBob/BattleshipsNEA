import math
from re import A


toDecrypt = "MZZZZ"
finRev = []
for x in range(len(toDecrypt) - 1, 0, -1):
    a = ord(toDecrypt[x])
    b = ord(toDecrypt[x-1])
    c = a - b
    finRev.append(chr(((c-1)%26) + 65))

finRev.append(toDecrypt[0])
finRev.reverse()

print("".join(finRev))

math
A