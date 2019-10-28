# forensic_350_investigative_reversing_2

------

### Titre : Investigative Reversing 2

### Points : 350

------

### Description

------

We have recovered a binary and an image See what you can make of it. There should be a flag somewhere. Its also found in /problems/investigative-reversing-2_5_b294e24c9063edbf722b9554e7750d19 on the shell server.

#### Hints

* Try using some forensics skills on the image
* This problem requires both forensics and reversing skills
* What is LSB encoding?

------

### Résolution

---

```bash
$ file mystery 
mystery: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/l, for GNU/Linux 3.2.0, BuildID[sha1]=2d2155d1fe9b3de7809f36ce63468d6e9a9ebbf7, not stripped

$ file encoded.bmp 
encoded.bmp: PC bitmap, Windows 3.x format, 1765 x 852 x 8
```

Le flag est sûrement caché dans l'image.

```c
undefined8 main(void) {
  long lVar1;
  FILE *fd_flag;
  FILE *img_input;
  FILE *img_output;
  size_t sVar2;
  ulong uVar3;
  long in_FS_OFFSET;
  byte readed_img_char;
  char new_char;
  int local_7c;
  int i;
  int j;
  int index;
  FILE *flag_fd;
  char flag [56];
  
  lVar1 = *(long *)(in_FS_OFFSET + 0x28);
  fd_flag = fopen("flag.txt","r");
  img_input = fopen("original.bmp","r");
  img_output = fopen("encoded.bmp","a");
  if (fd_flag == (FILE *)0x0) {
    puts("No flag found, please make sure this is run on the server");
  }
  if (img_input == (FILE *)0x0) {
    puts("original.bmp is missing, please run this on the server");
  }
  sVar2 = fread(&readed_img_char,1,1,img_input);
  local_7c = (int)sVar2;
  i = 0;
  while (i < 2000) {
    fputc((int)(char)readed_img_char,img_output);
    sVar2 = fread(&readed_img_char,1,1,img_input);
    local_7c = (int)sVar2;
    i = i + 1;
  }
  sVar2 = fread(flag,0x32,1,fd_flag);
  if ((int)sVar2 < 1) {
    puts("flag is not 50 chars");
                    /* WARNING: Subroutine does not return */
    exit(0);
  }
  j = 0;
  while (j < 0x32) {
    index = 0;
    while (index < 8) {
      uVar3 = codedChar(index,flag[(long)j] - 5,readed_img_char);
      fputc((int)(char)uVar3,img_output);
      fread(&readed_img_char,1,1,img_input);
      index = index + 1;
    }
    j = j + 1;
  }
  while (local_7c == 1) {
    fputc((int)(char)readed_img_char,img_output);
    sVar2 = fread(&readed_img_char,1,1,img_input);
    local_7c = (int)sVar2;
  }
  fclose(img_output);
  fclose(img_input);
  fclose(fd_flag);
  if (lVar1 == *(long *)(in_FS_OFFSET + 0x28)) {
    return 0;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}
```

```c
ulong codedChar(int index,byte char,byte readed_char) {
  byte local_20;
  
  local_20 = char;
  if (index != 0) {
    local_20 = (byte)((int)(char)char >> ((byte)index & 0x1f));
  }
  return (ulong)(readed_char & 0xfe | local_20 & 1);
}
```

Le flag se trouve dans `flag.txt`, l'image de base est `original.bmp`, et l'image qui va contenir le flag est `encoded.bmp` (celle que nous possédons).

Les 2000 premiers octets de `original.bmp` sont copiés tels quels dans `encoded.bmp`. Puis nous cachons les `0x32` caractères du flag aux quels nous ajoutons un chiffrement par décalage de `-5`. Nous cachons le flag bit par bit en commencant par les bits de poids faibles.

Nous savons que le flag fait `0x32` (50) caractères.

```python
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
```

```bash
$ python3 resolv.py 
picoCTF{n3xt_0n30000000000000000000000000f69eb8c8}
```

`picoCTF{n3xt_0n30000000000000000000000000f69eb8c8}`