# forensic_500_investigation_encoded_2

------

### Titre : investigation_encoded_2

### Points : 500

------

### Description

------

We have recovered a binary and 1 file: image01. See what you can make of it. Its also found in /problems/investigation-encoded-2_0_bf594e1542e760d4c72cc1401d71b3eb on the shell server. NOTE: The flag is not in the normal picoCTF{XXX} format.

#### Hints

* Only use lower case letters and numbers

------

### Résolution

---

```bash
$ file mystery
mystery: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/l, for GNU/Linux 3.2.0, BuildID[sha1]=b3214ef986bc85652feb1040e5970f356b56dd71, not stripped

$ xxd output_flag 
00000000: baa3 aebb 8a3a ab8e aa3a ebb8 ea8e aae2  .....:...:......
00000010: eae8 eab8 eab8 eab8 eab8 eab8 eab8 eab8  ................
00000020: eab8 eab8 eab8 eab8 eaae 2ab8 eae8 bae8  ..........*.....
00000030: aeea 2bbb 8bae 8eab 80                   ..+......
```

```c
undefined8 main(void) {
  long lVar1;
  size_t sVar2;
  undefined4 local_18;
  int local_14;
  FILE *fd_flag;
  
  badChars = '\0';
  fd_flag = fopen("flag.txt","r");
  if (fd_flag == (FILE *)0x0) {
    fwrite("Error: file ./flag.txt not found\n",1,0x21,stderr);
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  flag_size = 0;
  fseek(fd_flag,0,2);
  lVar1 = ftell(fd_flag);
  flag_size = (int)lVar1;
  fseek(fd_flag,0,0);
  login();
  if (0xfffe < flag_size) {
    fwrite("Error, file bigger than 65535\n",1,0x1e,stderr);
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  flag = malloc((long)flag_size);
  sVar2 = fread(flag,1,(long)flag_size,fd_flag);
  local_14 = (int)sVar2;
  if (local_14 < 1) {
                    /* WARNING: Subroutine does not return */
    exit(0);
  }
  local_18 = 0;
  flag_index = &local_18;
  output = fopen("output","w");
  buffChar = 0;
  remain = 7;
  fclose(fd_flag);
  encode();
  fclose(output);
  if (badChars == '\x01') {
    fwrite("Invalid Characters in flag.txt\n./output is corrupted\n",1,0x35,stderr);
  }
  else {
    fwrite("I\'m Done, check file ./output\n",1,0x1e,stderr);
  }
  return 0;
}
```

```c
void login(void) {
  int iVar1;
  undefined8 local_c8;
  undefined8 local_c0;
  undefined8 local_b8;
  undefined8 local_b0;
  undefined8 local_a8;
  undefined8 local_a0;
  undefined8 local_98;
  undefined8 local_90;
  undefined8 local_88;
  undefined8 local_80;
  undefined8 local_78;
  undefined8 local_70;
  undefined4 local_68;
  char local_58 [48];
  sa_family_t local_28;
  uint16_t local_26;
  undefined auStack36 [12];
  int local_18;
  int local_14;
  hostent *local_10;
  
  local_10 = gethostbyname("ZmFrZWF1dGhzaXRl.com"); // fakeauthsite
  local_14 = socket(2,1,0);
  local_28 = 2;
  local_26 = htons(0x929);
  bcopy(*local_10->h_addr_list,&local_28 + 4,(long)local_10->h_length);
  local_18 = connect(local_14,(sockaddr *)&local_28,0x10);
  if (local_18 == -1) {
    puts("Could not connect to Auth Server");
  }
  local_c8 = 0x6e43203a68747541;
  local_c0 = 0x33636c78575a7a56;
  local_b8 = 0x53593046475a674d;
  local_b0 = 0x6d61687057597142;
  local_a8 = 0x4b45;
  local_a0 = 0;
  local_98 = 0;
  local_90 = 0;
  local_88 = 0;
  local_80 = 0;
  local_78 = 0;
  local_70 = 0;
  local_68 = 0;
  send(local_14,&local_c8,100,0);
  recv(local_14,local_58,0x21,0);
  iVar1 = strcmp(local_58,"QXV0aG9yaXplZCB0byBleGVjdXRlLi4u"); // Authorized to execute...
  if (iVar1 != 0) {
    puts("Permission not given by the Auth Server");
    printf(" answer: %s\n",local_58);
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  printf(" answer: %s\n",local_58);
  shutdown(local_14,2);
  return;
}
```

```c
void encode(void) {
  byte bVar1;
  ulong uVar2;
  int iVar3;
  int res1;
  char falag_char;
  int res2;
  
  while (*flag_index < flag_size) {
    uVar2 = lower(*(byte *)((long)*flag_index + flag));
    falag_char = (char)uVar2;
    if (falag_char == ' ') {
      falag_char = -0x7b;
    }
    else {
      if (('/' < falag_char) && (falag_char < ':')) {
        falag_char = falag_char + 'K';
      }
    }
    falag_char = falag_char + -0x61;
    if ((falag_char < '\0') || ('$' < falag_char)) {
      badChars = 1;
    }
    if (falag_char != '$') {
      iVar3 = ((int)falag_char + 0x12) % 0x24;
      bVar1 = (byte)(iVar3 >> 0x1f);
      falag_char = ((byte)iVar3 ^ bVar1) - bVar1;
    }
    res1 = *(int *)(indexTable + (long)(int)falag_char * 4);
    res2 = *(int *)(indexTable + (long)((int)falag_char + 1) * 4);
    while (res1 < res2) {
      uVar2 = getValue(res1);
      save((byte)uVar2);
      res1 = res1 + 1;
    }
    *flag_index = *flag_index + 1;
  }
  while (remain != 7) {
    save(0);
  }
  return;
}
```

```c
ulong lower(byte c) {
  ulong uVar1;
  
  if (((char)c < 'A') || ('Z' < (char)c)) {
    uVar1 = (ulong)c;
  }
  else {
    uVar1 = (ulong)((uint)c + 0x20);
  }
  return uVar1;
}
```

```c
ulong getValue(int c) {
  byte bVar1;
  int iVar2;
  
  iVar2 = c;
  if (c < 0) {
    iVar2 = c + 7;
  }
  bVar1 = (byte)(c >> 0x37);
  return (ulong)((int)(uint)(byte)secret[(long)(iVar2 >> 3)] >>
                 (7 - (((char)c + (bVar1 >> 5) & 7) - (bVar1 >> 5)) & 0x1f) & 1);
}
```

```c
void save(byte c) {
  buffChar = buffChar | c;
  if (remain == 0) {
    remain = 7;
    fputc((int)(char)buffChar,output);
    buffChar = '\0';
  }
  else {
    buffChar = buffChar * '\x02';
    remain = remain + -1;
  }
  return;
}
```

```python
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
```

Même technique que pour `forensic_0450_investigation_encoded_1`. On réalise une attaque de brute force.

```bash
$ python3 resolv.py 
t
t1
t1m
t1m3
t1m3f
t1m3f1
t1m3f1i
t1m3f1i3
t1m3f1i35
t1m3f1i350
t1m3f1i3500
t1m3f1i35000
t1m3f1i350000
t1m3f1i3500000
t1m3f1i35000000
t1m3f1i350000000
t1m3f1i3500000000
t1m3f1i35000000000
t1m3f1i350000000000
t1m3f1i3500000000000
t1m3f1i35000000000003
t1m3f1i35000000000003d
t1m3f1i35000000000003d7
t1m3f1i35000000000003d74
t1m3f1i35000000000003d746
t1m3f1i35000000000003d746a
t1m3f1i35000000000003d746a4
t1m3f1i35000000000003d746a40
```

`t1m3f1i35000000000003d746a40`