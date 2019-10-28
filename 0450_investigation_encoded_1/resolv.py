#!/usr/bin/env python3

import string
import sys

secret = 'b8ea8eba3a88ae8ee8aa28bbb8eb8ba8ee3a3bb8bba3bae2e8a8e2b8ab8bb8eae3aee3ba80'
secret = [int(secret[i:i+2],16) for i in range(0, len(secret), 2)]

matrix = '08000000000000000c000000080000000e000000140000000a00000022000000040000002c0000000c000000300000000c0000003c0000000a00000048000000060000005200000010000000580000000c000000680000000c000000740000000a00000080000000080000008a0000000e000000920000000e000000a000000010000000ae0000000a000000be00000008000000c800000006000000d00000000a000000d60000000c000000e00000000c000000ec0000000e000000f800000010000000060100000e000000160100000400000024010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
matrix = [int(matrix[i:i+2],16) for i in range(0, len(matrix), 2)]

cipher = open('output_flag', 'rb').read()
cipher = ''.join([bin(b)[2:].zfill(8) for b in cipher])

def getValue(res):
    var2 = res
    if res < 0:
        var2 = res + 7
    var1 = res >> 0x37
    return secret[var2 >> 3] >> (7 - ((res + (var1 >> 5) & 7) - (var1 >> 5)) & 0x1f) & 1

def lower(c):
    if chr(c) not in string.ascii_lowercase:
        c = c + 0x20
    return c


charset = string.ascii_lowercase
possibles = []
flag = ''
index = 0
commun = 0
while 1:
    possibles = []
    for c0 in charset:
        for c1 in charset:
            flag = flag[:index] + c0 + c1
            output = ''
            for c in flag.encode():
                c = lower(c)
                if c == b' ':
                    c = b'{'
                res1 = matrix[(c - 0x61) * 8 + 4]
                
                res2 = res1 + matrix[(c - 0x61)*8]
                
                while res1 < res2:
                    output += str(getValue(res1))
                    res1 += 1
            if output[:commun] == cipher[:commun]:
                possibles.append(flag)
    if len(possibles) == 1:
        flag = flag[:index] + possibles[0][-2]
        print(flag)
        index += 1
        commun += 3
    else:
        commun += 1
