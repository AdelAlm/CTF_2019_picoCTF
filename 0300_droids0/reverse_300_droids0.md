# reverse_300_droids0

------

### Titre : droids0

### Points : 300

------

### Description

------

Where do droid logs go. Check out this file. You can also find the file in /problems/droids0_0_205f7b4a3b23490adffddfcfc45a2ca3.

#### Hints

* Try using an emulator or device
* https://developer.android.com/studio

------

### Résolution

---

```bash
$ file zero.apk 
zero.apk: Zip archive data, at least v1.0 to extract
```

Nous allons utiliser `anbox` pour émuler un système Android. Il faut penser à autoriser l'installation des applications non-officielles: `Settings > Security > Unknown sources > ON`.

Nous allons utiliser `adb` pour communiquer avec notre `anbox`.

> Android Debug Bridge (adb) is a versatile command line  tool  that  lets  you communicate  with  an  emulator instance or connected Android-powered device.

```bash
# lister nos devices
$ adb devices
List of devices attached
emulator-5558   device

# si besoin
$ adb uninstall com.hellocmu.picoctf 
Success
```

```bash
$ adb install zero.apk 
Success
```

On installe notre apk avec `adb`. L'application demande un mot de passe pour obtenir le flag. D'après, la description du challenge, il faut chercher des données dans les logs. Nous allons lancer l'application et regarder les logs qu'elle crée.

```bash
$ adb --help
...
logcat                   show device log (logcat --help for more)
...
$ adb logcat
09-28 08:40:42.017   115   756 E SoundPool: Unable to load sample
09-28 08:40:45.645   667   667 I PICO    : picoCTF{a.moose.once.bit.my.sister}
09-28 08:40:45.667    39    97 I MediaPlayerService: MediaPlayerService::getOMX
```

En suivant les logs lorsque l'on soumet un mot de passe, on peut voir un flag sauvage qui apparaît.

`picoCTF{a.moose.once.bit.my.sister}`