#!/usr/bin/env python3

import subprocess as sp

cmd = sp.Popen('r2 -Ad test', stdin=sp.PIPE, stdout=sp.PIPE, shell=True)
print(cmd.stdout.read())
cmd.stdin.write(b's sym.init_randomness\n')

# db 0x55b33de6eaee // break in init_random
# db 0x55b33de6edf5 // break in cmp rax, rdx 
# dc
# dr rax=0x5d8f5586
# dc
# dc
# dc
# 123
# dr eax
# 0x572b6058

