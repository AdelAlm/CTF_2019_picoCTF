#!/usr/bin/env python3

f = b'picoCTF{w1{1wq8c5ajc<a5}'

print(f[:8].decode(), end='')
for i in range(8, len(f)-1):
    if (i & 1) == 0:
        print(chr(f[i] - 0x5), end='')
    else:
        print(chr(f[i] + 2), end='')
print('}')
