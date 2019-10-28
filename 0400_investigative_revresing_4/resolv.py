#!/usr/bin/env python3

res = ''
for c in '54321':
    f = open(f'Item0{c}_cp.bmp', 'rb')
    f.seek(0x7e3)

    char = f.read(1)
    j = 0
    while j < 0x32:
        if (j % 5) == 0:
            index = 0
            while index < 8:
                res += bin(ord(char))[-1]
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

# 5 to 1
# src -> Item05_cp.bmp
# dest -> Item05.bmp
