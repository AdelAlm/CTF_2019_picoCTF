# forensic_400_investigative_reversing_4

------

### Titre : Investigative Reversing 4

### Points : 400

------

### Description

------

We have recovered a binary and 5 images: image01, image02, image03, image04, image05. See what you can make of it. There should be a flag somewhere. Its also found in /problems/investigative-reversing-4_4_065969419be9af8229e29d22453a06d0 on the shell server.

#### Hints

* 

------

### Résolution

---

```bash
$ file mystery 
mystery: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/l, for GNU/Linux 3.2.0, BuildID[sha1]=b671dc4e37510bec651d650ed78ea135f8cdf702, not stripped

$ file Item0*
Item01_cp.bmp: PC bitmap, Windows 3.x format, 1765 x 852 x 8
Item02_cp.bmp: PC bitmap, Windows 3.x format, 1765 x 852 x 8
Item03_cp.bmp: PC bitmap, Windows 3.x format, 1765 x 852 x 8
Item04_cp.bmp: PC bitmap, Windows 3.x format, 1765 x 852 x 8
Item05_cp.bmp: PC bitmap, Windows 3.x format, 1765 x 852 x 8
```

Cette fois nous avons plusieurs images.

```c
undefined8 main(void) {
  size_t sVar1;
  undefined4 local_4c;
  undefined local_48 [52];
  int local_14;
  FILE *flag_fd;
  
  flag = local_48;
  local_4c = 0;
  flag_index = &local_4c;
  flag_fd = fopen("flag.txt","r");
  if (flag_fd == (FILE *)0x0) {
    puts("No flag found, please make sure this is run on the server");
  }
  sVar1 = fread(flag,0x32,1,flag_fd);
  local_14 = (int)sVar1;
  if (local_14 < 1) {
    puts("Invalid Flag");
                    /* WARNING: Subroutine does not return */
    exit(0);
  }
  fclose(flag_fd);
  encodeAll();
  return 0;
}
```

Ce challenge est proche du précédent, c'est juste la manière de cacher les données qui va changer.

```c
void encodeAll(void) {
  ulong item01;
  ulong local_28;
  undefined8 bmp;
  undefined4 local_18;
  char index;
  
  local_28 = 0x635f31306d657449;
  bmp = 0x706d622e70;
  local_18 = 0;
  item01 = 0x622e31306d657449;
  index = '5';
  while ('0' < index) {
    item01._0_6_ = CONCAT15(index,(undefined5)item01);
    item01 = item01 & 0xffff000000000000 | (ulong)(uint6)item01;
    local_28._0_6_ = CONCAT15(index,(undefined5)local_28);
    local_28 = local_28 & 0xffff000000000000 | (ulong)(uint6)local_28;
    encodeDataInFile((char *)&item01,(char *)&local_28);
    index = index + -1;
  }
  return;
}
```

Les données sont cachées successivement dans les 5 images.

```c
void encodeDataInFile(char *param_1,char *param_2) {
  FILE *src;
  FILE *dest;
  size_t sVar1;
  ulong uVar2;
  byte readed_char;
  int limit;
  FILE *dst;
  FILE *img_src;
  int index;
  int j;
  int i;
  int local_c;
  
  src = fopen(param_1,"r");
  dest = fopen(param_2,"a");
  if (src != (FILE *)0x0) {
    sVar1 = fread(&readed_char,1,1,src);
    local_c = (int)sVar1;
    i = 0;
    while (i < 0x7e3) {
      fputc((int)(char)readed_char,dest);
      sVar1 = fread(&readed_char,1,1,src);
      local_c = (int)sVar1;
      i = i + 1;
    }
    j = 0;
    while (j < 0x32) {
      if (j % 5 == 0) {
        index = 0;
        while (index < 8) {
          uVar2 = codedChar(index,*(byte *)((long)*flag_index + flag),readed_char);
          fputc((int)(char)uVar2,dest);
          fread(&readed_char,1,1,src);
          index = index + 1;
        }
        *flag_index = *flag_index + 1;
      }
      else {
        fputc((int)(char)readed_char,dest);
        fread(&readed_char,1,1,src);
      }
      j = j + 1;
    }
    while (local_c == 1) {
      fputc((int)(char)readed_char,dest);
      sVar1 = fread(&readed_char,1,1,src);
      local_c = (int)sVar1;
    }
    fclose(dest);
    fclose(src);
    return;
  }
  puts("No output found, please run this on the server");
                    /* WARNING: Subroutine does not return */
  exit(0);
}
```

Ajout des données dans l'image.

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

Extraction des données de chaque image.

```bash
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
```

```bash
$ python3 resolv.py 
picoCTF{N1c3_R3ver51ng_5k1115_000000000008d246eaf}
```

`picoCTF{N1c3_R3ver51ng_5k1115_000000000008d246eaf}`