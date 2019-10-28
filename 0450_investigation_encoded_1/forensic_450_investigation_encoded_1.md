# forensic_450_investigation_encoded_1

------

### Titre : c0rrupt

### Points : 450

------

### Description

------

We have recovered a binary and 1 file: image01. See what you can make of it. Its also found in /problems/investigation-encoded-1_6_172edc378b5282150ec24be19ff8342b on the shell server. NOTE: The flag is not in the normal picoCTF{XXX} format.

#### Hints

* 

------

### Résolution

---

```bash
$ file mystery 
mystery: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/l, for GNU/Linux 3.2.0, BuildID[sha1]=29b4dba83a1a5a26d76e122ad48d63cff886b075, not stripped

$ xxd output
00000000: 8e8e ba3b b8ea 23a8 ee8e ae3b 8ae2 e8aa  ...;..#....;....
00000010: 38ae 3bb8 ae00
```

```c
undefined8 main(void) {
  long size;
  size_t sVar1;
  undefined4 i;
  int local_14;
  FILE *flag_fd;
  
  flag_fd = fopen("flag.txt","r");
  if (flag_fd == (FILE *)0x0) {
    fwrite("./flag.txt not found\n",1,0x15,stderr);
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  flag_size = 0;
  fseek(flag_fd,0,2);
  size = ftell(flag_fd);
  flag_size = (int)size;
  fseek(flag_fd,0,0);
  if (0xfffe < flag_size) {
    fwrite("Error, file bigger that 65535\n",1,0x1e,stderr);
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  flag = malloc((long)flag_size);
  sVar1 = fread(flag,1,(long)flag_size,flag_fd);
  local_14 = (int)sVar1;
  if (local_14 < 1) {
                    /* WARNING: Subroutine does not return */
    exit(0);
  }
  i = 0;
  flag_index = &i;
  output = fopen("output","w");
  buffChar = 0;
  remain = 7;
  fclose(flag_fd);
  encode();
  fclose(output);
  fwrite("I\'m Done, check ./output\n",1,0x19,stderr);
  return 0;
}
```

Lecture du `flag.txt` et on appelle `encode()`.

```c
void encode(void) {
  int iVar1;
  undefined8 uVar2;
  ulong new_char_int;
  ulong uVar3;
  int local_10;
  char new_char;
  byte char;
  
  while( true ) {
    if (flag_size <= *flag_index) {
      while (remain != 7) {
        save(0);
      }
      return;
    }
    char = *(byte *)((long)*flag_index + flag);
    uVar2 = isValid(char);
    if ((char)uVar2 != '\x01') break;
    new_char_int = lower(char);
    new_char = (char)new_char_int;
    if (new_char == ' ') {
      new_char = '{';
    }
    local_10 = *(int *)(matrix + (long)((int)new_char + -0x61) * 8 + 4);
    iVar1 = local_10 + *(int *)(matrix + (long)((int)new_char + -0x61) * 8);
    while (local_10 < iVar1) {
      uVar3 = getValue(local_10);
      save((byte)uVar3);
      local_10 = local_10 + 1;
    }
    *flag_index = *flag_index + 1;
  }
  fwrite("Error, I don\'t know why I crashed\n",1,0x22,stderr);
                    /* WARNING: Subroutine does not return */
  exit(1);
}
```

```c
undefined8 isValid(char c) {
  undefined8 uVar1;
  
  if ((c < 'a') || ('z' < c)) {
    if ((c < 'A') || ('Z' < c)) {
      if (c == ' ') {
        uVar1 = 1;
      }
      else {
        uVar1 = 0;
      }
    }
    else {
      uVar1 = 1;
    }
  }
  else {
    uVar1 = 1;
  }
  return uVar1;
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
ulong getValue(int char) {
  byte bVar1;
  int iVar2;
  
  iVar2 = char;
  if (char < 0) {
    iVar2 = char + 7;
  }
  bVar1 = (byte)(char >> 0x37);
  return (ulong)((int)(uint)(byte)secret[(long)(iVar2 >> 3)] >>
                 (7 - (((char)char + (bVar1 >> 5) & 7) - (bVar1 >> 5)) & 0x1f) & 1);
}
```

```c
void save(byte char) {
  buffChar = buffChar | char;
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

Pour faire simple, c'est une fonction qui va chiffrer le contenu de `flag.txt`.

Pour résoudre ce challenge, nous allons ré-implémenter le chiffrement en python et réaliser une attaque brute force sur le chiffré et comparé à chaque fois avec le chiffré du flag que nous possédons. 

```python
#!/usr/bin/env python3                                                  
                                                                        
import string                                                           
import sys                                                              
                                                                        
secret = 'b8ea8eba3a88ae8ee8aa28bbb8eb8ba8ee3a3bb8bba3bae2e8a8e2b8ab8bb8
eae3aee3ba80'                                                           
secret = [int(secret[i:i+2],16) for i in range(0, len(secret), 2)]      
                                                                        
matrix = '08000000000000000c000000080000000e000000140000000a00000022000000040000002c0000000c000000300000000c0000003c0000000a00000048000000060000005200000010000000580000000c000000680000000c000000740000000a00000080000000080000008a0000000e000000920000000e000000a000000010000000ae0000000a000000be00000008000000c800000006000000d00000000a000000d60000000c000000e00000000c000000ec0000000e000000f800000010000000060100000e000000160100000400000024010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'                               
matrix = [int(matrix[i:i+2],16) for i in range(0, len(matrix), 2)]      
                                                                        
cipher = open('output_flag', 'rb').read()                               
cipher = ''.join([bin(b)[2:].zfill(8) for b in cipher])

def getValue(res):
    var2 = res
    if res < 0:
        var2 = res + 7
    var1 = res >> 0x37
    return secret[var2 >> 3] >> (7 - ((res + (var1 >> 5) & 7) - (var1 >> 5)) & 0x1f) & 1

def lower(c):
    if chr(c) not in string.ascii_lowercase:
        c = c + 0x20
    return c

charset = string.ascii_lowercase
possibles = []
flag = ''
index = 0
commun = 0
while 1:
    possibles = []
    for c0 in charset:
        for c1 in charset:
            flag = flag[:index] + c0 + c1
            output = ''
            for c in flag.encode():
                c = lower(c)
                if c == b' ':
                    c = b'{'
                res1 = matrix[(c - 0x61) * 8 + 4]
                
                res2 = res1 + matrix[(c - 0x61)*8]
                
                while res1 < res2:
                    output += str(getValue(res1))
                    res1 += 1
            if output[:commun] == cipher[:commun]:
                possibles.append(flag)
    if len(possibles) == 1:
        flag = flag[:index] + possibles[0][-2]
        print(flag)
        index += 1
        commun += 3
    else:
        commun += 1
```

Le but est de tester petit à petit des petits blocs de clair, puis de les chiffrer et de comparer avec une partie de `output_flag`, si une seule entrant est possible alors on considère que cette entrée est bonne et on avance.

```bash
$ python3 resolv.py
e
en
enc
enco
encod
encode
encoded
encodedg
encodedgx
encodedgxm
encodedgxmu
encodedgxmur
encodedgxmurh
encodedgxmurht
encodedgxmurhtu
encodedgxmurhtuo
encodedgxmurhtuou
```

`encodedgxmurhtuou`
