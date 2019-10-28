# reverse_350_droids1

------

### Titre : droids1

### Points : 350

------

### Description

------

Find the pass, get the flag. Check out this file. You can also find the file in /problems/droids1_0_b7f94e21c7e45e6604972f9bc3f50e24.

#### Hints

* Try using an emulator or device
* https://ibotpeaches.github.io/Apktool/
* https://developer.android.com/studio

------

### Résolution

---

```bash
$ file one.apk 
one.apk: Zip archive data, at least v1.0 to extract
```

Nous allons utiliser `jadx` pour reverser notre `apk`.

```java
// MainActivity
public void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView((int) C0272R.layout.activity_main);
    this.text_top = (TextView) findViewById(C0272R.C0274id.text_top);
    this.text_bottom = (TextView) findViewById(C0272R.C0274id.text_bottom);
    this.text_input = (EditText) findViewById(C0272R.C0274id.text_input);
    this.ctx = getApplicationContext();
    System.loadLibrary("hellojni");
    this.text_top.setText(C0272R.string.hint);
}

public void buttonClick(View view) { 	       	this.text_bottom.setText(FlagstaffHill.getFlag(this.text_input.getText().toString(), this.ctx));
}
```

C'est un `MainActivity` classique, lorsque l'on appuis sur le bouton, nous appelons `FlagstaffHill.getFlag(input)`.

```java
// FlagstaffHill
public static native String fenugreek(String str);
public static String getFlag(String input, Context ctx) {
    if (input.equals(ctx.getString(C0272R.string.password))) {
        return fenugreek(input);
    }
    return "NOPE";
}
```

Notre `input` est comparée à `C0272R.string.password`. Nous devons alors trouver sa valeur.

```bash
# avec jadx-gui
# Resources > resources.arcs > res > values > strings.xml
<string name="myotis">jackrabbit</string>
<string name="password">opossum</string>
<string name="porcupine">blackbuck</string>

# en cli
$ cat one/res/values/strings.xml | grep password
<string name="password">opossum</string>
```

Le mot de passe est donc `opossum`.

```bash
$ adb devices
List of devices attached
emulator-5558   device

# si besoin
$ adb uninstall com.hellocmu.picoctf 
Success
```

```bash
$ adb install one.apk 
Success
```

En fournissant le mot de passe, on obtient le flag.

`picoCTF{pining.for.the.fjords}`