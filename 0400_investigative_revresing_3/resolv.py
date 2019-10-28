#!/usr/bin/env python3

f = open('encoded.bmp', 'rb')

# skip 0x2d3 bytes
f.seek(0x2d3)

# extract bits
res = ''
char = f.read(1)
j = 0
while j < 100:
    if (j & 1) == 0:
        index = 0
        while index < 8:
            res +=  bin(ord(char))[-1]
            char = f.read(1)
            index += 1
    else:
        char = f.read(1)
    j += 1

# bytes blocks
res = [res[i:i+8] for i in range(0, len(res), 8)]

# inverse
res = [b[::-1] for b in res]

# to int
res = [int(b,2) for b in res]

print(''.join([chr(b) for b in res]))
