#!/usr/bin/env python3

import sys
import string
import binascii
import subprocess as sp


cipher = bin(int(binascii.hexlify(open('output_flag', 'rb').read()),16))[2:]

charset = string.ascii_lowercase + string.digits + ' '

flag = ''
possibles = []
commun = 3
index = 0
while 1:
    possibles = []
    for c in charset:
        sp.run(f'echo -n "{flag + c}" > flag.txt 2> /dev/null', shell=True)
        sp.run('./mystery_patched 2> /dev/null', shell=True)
        out = bin(int(binascii.hexlify(open('output', 'rb').read()),16))[2:]
        if out[:commun] == cipher[:commun]:
            possibles.append(c)
    if len(possibles) == 1:
        flag = flag[:index] + possibles[0]
        print(flag)
        index += 1
        commun += 3
    else:
        commun += 1
