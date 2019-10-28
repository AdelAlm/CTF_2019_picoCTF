# reverse_400_droids2

------

### Titre : droids2

### Points : 400

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
$ file two.apk 
two.apk: Zip archive data, at least v1.0 to extract
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

public void buttonClick(View view) {
  this.text_bottom.setText(FlagstaffHill.getFlag(this.text_input.getText().toString(), this.ctx));
}
```

Lorsque l'on clique sur le bouton `FlagstaffHill.getFlag(input)` est appélé.

```java
// FlagstaffHill
public static native String sesame(String str);

public static String getFlag(String input, Context ctx) {
    String[] witches = {"weatherwax", "ogg", "garlick", "nitt", "aching", "dismass"};
    int second = 3 - 3;
    int third = (3 / 3) + second;
    int fourth = (third + third) - second;
    int fifth = 3 + fourth;
    int sixth = (fifth + second) - third;
    String str = ".";
    if (input.equals("".concat(witches[fifth]).concat(str).concat(witches[third]).concat(str).concat(witches[second]).concat(str).concat(witches[sixth]).concat(str).concat(witches[3]).concat(str).concat(witches[fourth]))) {
        return sesame(input);
	}
    return "NOPE";
}
```

Notre `input` est comparé à une chaine construite à partir du tablea `witches`. Nous allons juste exécuter le code pour récupérer la sortie.

```java
class Test {

  public static void main(String[] args){
      
      String[] witches = {"weatherwax", "ogg", "garlick", "nitt", "aching", "dismass"};
      int second = 3 - 3;
      int third = (3 / 3) + second;
      int fourth = (third + third) - second;
      int fifth = 3 + fourth;
      int sixth = (fifth + second) - third;
      String str = ".";
      System.out.println("".concat(witches[fifth]).concat(str).concat(witches[third]).concat(str).concat(witches[second]).concat(str).concat(witches[sixth]).concat(str).concat(witches[3]).concat(str).concat(witches[fourth]));
        
  }
}
```

```bash
$ java resolv.java
dismass.ogg.weatherwax.aching.nitt.garlick
```

Nous devons donc fournir `dismass.ogg.weatherwax.aching.nitt.garlick` dans l'input de l'application.

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

Cela nous permet de récupérer le flag.

`picoCTF{what.is.your.favourite.colour}`