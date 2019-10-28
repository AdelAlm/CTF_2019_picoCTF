# reverse_300_reverse_cipher

------

### Titre : reverse_cipher

### Points : 300

------

### Description

------

We have recovered a binary and a text file. Can you reverse the flag. Its also found in /problems/reverse-cipher_5_6e21330f568439d366f5c038e32e5572 on the shell server.

#### Hints

* objdump and Gihdra are some tools that could assist with this

------

### Résolution

---

```bash
$ file rev
rev: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/l, for GNU/Linux 3.2.0, BuildID[sha1]=523d51973c11197605c76f84d4afb0fe9e59338c, not stripped

$ cat rev_this 
picoCTF{w1{1wq8c5ajc<a5}
```

Nous allons utiliser Ghidra pour analyser ce binaire.

```c
void main(void) {
  FILE *flag_fd;
  FILE *output;
  size_t sVar1;
  char flag [23];
  char local_41;
  FILE *output_fd;
  FILE *fd_flag;
  uint j;
  int i;
  char chr;
  
  flag_fd = fopen("flag.txt","r");
  output = fopen("rev_this","a");
  if (flag_fd == (FILE *)0x0) {
    puts("No flag found, please make sure this is run on the server");
  }
  if (output == (FILE *)0x0) {
    puts("please run this on the server");
  }
  sVar1 = fread(flag,0x18,1,flag_fd);
  if ((int)sVar1 < 1) {
                    /* WARNING: Subroutine does not return */
    exit(0);
  }
  i = 0;
  while (i < 8) {
    fputc((int)flag[(long)i],output);
    i = i + 1;
  }
  j = 8;
  while ((int)j < 0x17) {
    if ((j & 1) == 0) {
      chr = flag[(long)(int)j] + '\x05';
    }
    else {
      chr = flag[(long)(int)j] + -2;
    }
    fputc((int)chr,output);
    j = j + 1;
  }
  fputc((int)local_41,output);
  fclose(output);
  fclose(flag_fd);
  return;
}
```

Le programme ouvre `flag.txt`, le résultat sera stocké dans `rev_this`. On lis les `0x18` caractères du flag que l'on stocke dans `flag`. Pour les 8 premiers caractères du flag, on ne fait rien, cela correspond à `picoCTF{`. On applique un chiffrement par décalage sur le reste du flag en fonction de la valeur de `j`. Si `j` est pair, on applique un décalage de `-2`, s'il est impair, on applique un décalage de `+5`. Pour retrouver le flag, nous devons simplement inverser ce processus.

```python
#!/usr/bin/env python3

f = b'picoCTF{w1{1wq8c5ajc<a5}'

print(f[:8].decode(), end='')
for i in range(8, len(f)-1):
    if (i & 1) == 0:
        print(chr(f[i] - 0x5), end='')
    else:
        print(chr(f[i] + 2), end='')
print('}')
```

```bash
$ python3 resolv.py 
picoCTF{r3v3rs3e0cee7c0}
```

`picoCTF{r3v3rs3e0cee7c0}`