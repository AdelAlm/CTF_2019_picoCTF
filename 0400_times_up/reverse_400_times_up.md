# reverse_400_times_up

------

### Titre : Time's Up

### Points : 400

------

### Description

------

Time waits for no one. Can you solve this before time runs out? times-up, located in the directory at /problems/time-s-up_6_480d53541469436212e30dad5b4ce691.

#### Hints

* Can you interact with the program using a script?

------

### Résolution

---

```bash
$ file times-up 
times-up: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/l, for GNU/Linux 3.2.0, BuildID[sha1]=578bcd6434fc9bd11298e7fef6e2902881cc0aa9, not stripped
```

```bash
$ ./times-up 
Challenge: (((((1032183956) + (1878807778)) + ((225381224) + (1179303096))) - (((1045422336) + (139966371)) + ((1989694838) - (2085101076)))) + ((((1848464302) + (2061365002)) + ((982301632) + (1345392744))) + (((-996389106) + (1165844304)) + ((-2065118412) - (1569134458)))))
Setting alarm...
Solution? Alarm clock

$ ./times-up 
Challenge: (((((-564505372) + (-265076648)) - ((-1588598789) + (-677091508))) - (((1385700842) + (-226168746)) + ((-1254715774) + (-1502038778)))) + ((((-218273796) + (-1183636487)) - ((-1478479326) + (-1458546544))) - (((1876126944) + (730593023)) + ((-605076252) - (-324856014)))))
Setting alarm...
Solution? Alarm clock
```

```c
undefined8 main(void) {
  init_randomness();
  printf("Challenge: ");
  generate_challenge();
  putchar(10);
  fflush(stdout);
  puts("Setting alarm...");
  fflush(stdout);
  ualarm(5000,0);
  printf("Solution? ");
  __isoc99_scanf(&DAT_00100e68,&guess);
  if (guess == result) {
    puts("Congrats! Here is the flag!");
    system("/bin/cat flag.txt");
  }
  else {
    puts("Nope!");
  }
  return 0;
}
```

```c
void init_randomness(void) {
  int rand1;
  int rand2;
  int rand3;
  time_t current_time;
  
  current_time = time(NULL);
  srand((uint)current_time);
  rand1 = rand();
  rand2 = rand();
  rand3 = rand();
  seed = (long)(rand3 + rand1 * rand2);
  return;
}
```

Pour résoudre ce challenge nous devons rapidement calculer l'équation du programme. Ce dernier se bassant sur `time(NULL)`, les randoms sont alors prédictables.

Pour résoudre le challenge nous alons simuler une exécution dans le futur, changer la valeur de `time(NULL)` en valeur plus haute (nous pouvons utiliser un débugger comme `radare2` afin de placer un breakpoint puis de changer la valeur utilisée par le programme).

```bash
$ for i in `seq 20`; do ./times-up <<< 2637658868 ; done
...
Challenge: (((((-525414656) + (1028030560)) + ((792839653) + (1470238638))) - (((-1347283975) + (1163814534)) + ((908858000) + (68117937)))) + ((((-1952885388) - (-1041361602)) + ((1370964930) + (-62900633))) + (((617188784) + (-649058860)) + ((-800929568) + (1101730302)))))
Setting alarm...
Solution? Congrats! Here is the flag!
picoCTF{Gotta go fast. Gotta go FAST. #1626a7fb}
```

Nous allons ensuite sur le serveur qui possède le `flag.txt` afin de lui donner la bon résultat.

`picoCTF{Gotta go fast. Gotta go FAST. #1626a7fb}`