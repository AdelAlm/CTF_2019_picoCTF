# forensic_400_investigative_reversing_3

------

### Titre : Investigative Reversing 3

### Points : 400

------

### Description

------

We have recovered a binary and an image See what you can make of it. There should be a flag somewhere. Its also found in /problems/investigative-reversing-3_4_e9ac1257fd5c98754e88bca6c65a6d5a on the shell server.

#### Hints

* You will want to reverse how the LSB encoding works on this problem

------

### Résolution

---

```bash
$ file mystery 
mystery: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/l, for GNU/Linux 3.2.0, BuildID[sha1]=84b6f32deb8d6ef5099ab1fac1a24f3f273cfaa0, not stripped$ file mystery 
mystery: data

$ file encoded.bmp 
encoded.bmp: PC bitmap, Windows 3.x format, 1765 x 852 x 8
```

```c
undefined8 main(void) {
  long lVar1;
  FILE *fd_flag;
  FILE *img_src;
  FILE *img_dst;
  size_t sVar2;
  ulong new_char;
  long in_FS_OFFSET;
  byte readed_char;
  int local_7c;
  int i;
  uint j;
  int index;
  FILE *flag_fd;
  byte flag [56];
  
  lVar1 = *(long *)(in_FS_OFFSET + 0x28);
  fd_flag = fopen("flag.txt","r");
  img_src = fopen("original.bmp","r");
  img_dst = fopen("encoded.bmp","a");
  if (fd_flag == (FILE *)0x0) {
    puts("No flag found, please make sure this is run on the server");
  }
  if (img_src == (FILE *)0x0) {
    puts("No output found, please run this on the server");
  }
  sVar2 = fread(&readed_char,1,1,img_src);
  local_7c = (int)sVar2;
  i = 0;
  while (i < 0x2d3) {
    fputc((int)(char)readed_char,img_dst);
    sVar2 = fread(&readed_char,1,1,img_src);
    local_7c = (int)sVar2;
    i = i + 1;
  }
  sVar2 = fread(flag,0x32,1,fd_flag);
  if ((int)sVar2 < 1) {
    puts("Invalid Flag");
                    /* WARNING: Subroutine does not return */
    exit(0);
  }
  j = 0;
  while ((int)j < 100) {
    if ((j & 1) == 0) {
      index = 0;
      while (index < 8) {
        new_char = codedChar(index,flag[(long)((int)(j + (j >> 0x1f)) >> 1)],readed_char);
        fputc((int)(char)new_char,img_dst);
        fread(&readed_char,1,1,img_src);
        index = index + 1;
      }
    }
    else {
      fputc((int)(char)readed_char,img_dst);
      fread(&readed_char,1,1,img_src);
    }
    j = j + 1;
  }
  while (local_7c == 1) {
    fputc((int)(char)readed_char,img_dst);
    sVar2 = fread(&readed_char,1,1,img_src);
    local_7c = (int)sVar2;
  }
  fclose(img_dst);
  fclose(img_src);
  fclose(fd_flag);
  if (lVar1 == *(long *)(in_FS_OFFSET + 0x28)) {
    return 0;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}
```

Ce challenge est proche du précédent, c'est juste la manière de cacher les données qui va changer.

```c
  j = 0;
  while ((int)j < 100) {
    if ((j & 1) == 0) {
      index = 0;
      while (index < 8) {
        new_char = codedChar(index,flag[(long)((int)(j + (j >> 0x1f)) >> 1)],readed_char);
        fputc((int)(char)new_char,img_dst);
        fread(&readed_char,1,1,img_src);
        index = index + 1;
      }
    }
    else {
      fputc((int)(char)readed_char,img_dst);
      fread(&readed_char,1,1,img_src);
    }
    j = j + 1;
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

Le script suivant permet d'extraire les données cachées.

```bash
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
```

```bash
$ python3 resolv.py 
picoCTF{4n0th3r_L5b_pr0bl3m_00000000000009b6871eb}
```

`picoCTF{4n0th3r_L5b_pr0bl3m_00000000000009b6871eb}`