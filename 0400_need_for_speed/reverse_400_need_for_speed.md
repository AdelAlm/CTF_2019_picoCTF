# reverse_400_need_for_speed

------

### Titre : Need For Speed

### Points : 400

------

### Description

------

The name of the game is speed. Are you quick enough to solve this problem and keep it above 50 mph? need-for-speed.

#### Hints

* What is the final key?

------

### Résolution

---

```bash
$ file need-for-speed 
need-for-speed: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/l, for GNU/Linux 3.2.0, BuildID[sha1]=d01e199f92712e220af4ea6796c8ed4a0bbfcdf8, not stripped
```

```bash
$ ./need-for-speed 
Keep this thing over 50 mph!
============================

Creating key...
Not fast enough. BOOM!
```

Lorsque l'on exécute le binaire, on a le message suivant: `No fast anough`.

```c
undefined8 main(void) {
  header();
  set_timer();
  get_key();
  print_flag();
  return 0;
}
```

On peut voir qua dans les `main()`, avant l'appel à `get_key()`, il y a un appem à `set_timer()`.

```c
void header(void) {
  uint i;
  
  puts("Keep this thing over 50 mph!");
  i = 0;
  while (i < 0x1c) {
    putchar(0x3d);
    i = i + 1;
  }
  puts("\n");
  return;
}
```

```c
void set_timer(void) {
  __sighandler_t p_Var1;
  
  p_Var1 = __sysv_signal(0xe,alarm_handler);
  if (p_Var1 == (__sighandler_t)0xffffffffffffffff) {
    printf(
           "\n\nSomething bad happened here. \nIf running on the shell server\nPlease contact theadmins with \"need-for-speed.c:%d\".\n"
           ,0x3c);
                    /* WARNING: Subroutine does not return */
    exit(0);
  }
  alarm(1);
  return;
}
```

```bash
$ kill -l
...
14) SIGALRM
...
```

Le code met en place un signal `SIGALRM`.

```c
void get_key(void) {
  undefined8 k;
  
  puts("Creating key...");
  k = calculate_key();
  key = (undefined4)k;
  puts("Finished");
  return;
}
```

```c
undefined8 calculate_key(void) {
  int i;
  
  i = -0x2e081a88;
  do {
    i = i + -1;
  } while (i != -0x17040d44);
  return 0xe8fbf2bc;
}
```

C'est sûrement cette boucle qui nous fait perdre beaucoup de temps, pour au final pas grand chose, puisque l'on retourne toujours la même valeur.

```c
void print_flag(void) {
  puts("Printing flag:");
  decrypt_flag();
  puts(flag);
  return;
}
```

```c
void decrypt_flag(void) {
  uint uVar1;
  byte local_1c [16];
  uint i;
  
  i = 0;
  while (i < 0x37) {
    uVar1 = (uint)((int)i >> 0x1f) >> 0x1f;
    flag[(long)(int)i] = flag[(long)(int)i] ^ local_1c[(long)(int)((i + uVar1 & 1) - uVar1)];
    i = i + 1;
  }
  return;
}
```

Nous allons utiliser `radare2` pour débugger notre binaire, le but sera de changer le comportement de la fonction `calculate_key(void)` afin de na pas perdre de temps pendant l'exécution.

```assembly
$ r2 -dA need-for-speed 
> s sym.calculate_key
> pdf
> db 0x563b98854845
> dc
Keep this thing over 50 mph!
============================

Creating key...
hit breakpoint at: 563b98854845
> pdf
0x563b98854841      55             push rbp
0x563b98854842      4889e5         mov rbp, rsp
;-- rip:
0x563b98854845 b    c745fc78e5f7.  mov dword [local_4h], 0xd1f7e578
0x563b9885484c      836dfc01       sub dword [local_4h], 1
0x563b98854850      817dfcbcf2fb.  cmp dword [local_4h], 0xe8fbf2bc
0x563b98854857      75f3           jne 0x563b9885484c
0x563b98854859      8b45fc         mov eax, dword [local_4h]
0x563b9885485c      5d             pop rbp
0x563b9885485d      c3             ret
> afvd
var local_4h = 0x7ffdb081091c  0xb08109300000563b   ;V..0...
> afvd local_4h
pxr $w @rbp-0x4
> wx 0xe8fbf2bc @ rbp-0x4
> afvd
var local_4h = 0x7ffdb081091c  0xb0810930bcf2fbe8   ....0...
> dc
child stopped with signal 14
[+] SIGNAL 14 errno=0 addr=0x00000000 code=128 ret=0
hit breakpoint at: 563b98854845
[+] signal 14 aka SIGALRM received 0
> dc

Finished
Printing flag:
PICOCTF{Good job keeping bus #2eaa9f42 speeding along!}
```

Nous ajoutons un breakpoint et on modifie la valeur de `local_4h`.

`PICOCTF{Good job keeping bus #2eaa9f42 speeding along!}`