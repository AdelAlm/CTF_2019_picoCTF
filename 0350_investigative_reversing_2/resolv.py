#!/usr/bin/env python3

f = open('encoded.bmp', 'rb').read()

# skip the first 2000 bytes
start = 2000

# find the good size
end = start + (0x32*8)

# select data
data = f[start:end]

# extract the bits
res = ''
for i in range(len(data)):
    res += bin(data[i])[-1]

# bytes blocks
res = [res[i:i+8] for i in range(0, len(res), 8)]

# inverse
res = [b[::-1] for b in res]

# to int and remove offset
res = [int(b,2)+5 for b in res]

print(''.join([chr(b) for b in res]))
