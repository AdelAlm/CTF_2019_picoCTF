# reverse_500_droids4

------

### Titre : droids4

### Points : 500

------

### Description

------

Reverse the pass, patch the file, get the flag. Check out this file. You can also find the file in /problems/droids4_0_99ba4f323d3d194b5092bf43d97e9ce9.

#### Hints

* 

------

### Résolution

---

```bash
$ file four.apk 
three.apk: Zip archive data, at least v1.0 to extract
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

```java
// FlagstaffHill
public static native String cardamom(String str);

public static String getFlag(String input, Context ctx) {
    String str = "aaa";
    StringBuilder ace = new StringBuilder(str);
    StringBuilder jack = new StringBuilder(str);
    StringBuilder queen = new StringBuilder(str);
    StringBuilder king = new StringBuilder(str);
    ace.setCharAt(0, (char) (ace.charAt(0) + 4));
    ace.setCharAt(1, (char) (ace.charAt(1) + 19));
    ace.setCharAt(2, (char) (ace.charAt(2) + 18));
    jack.setCharAt(0, (char) (jack.charAt(0) + 7));
    jack.setCharAt(1, (char) (jack.charAt(1) + 0));
    jack.setCharAt(2, (char) (jack.charAt(2) + 1));
    queen.setCharAt(0, (char) (queen.charAt(0) + 0));
    queen.setCharAt(1, (char) (queen.charAt(1) + 11));
    queen.setCharAt(2, (char) (queen.charAt(2) + 15));
    king.setCharAt(0, (char) (king.charAt(0) + 14));
    king.setCharAt(1, (char) (king.charAt(1) + 20));
    king.setCharAt(2, (char) (king.charAt(2) + 15));
    
    if (input.equals("".concat(queen.toString()).concat(jack.toString()).concat(ace.toString()).concat(king.toString()))) {
        return "call it";
    }
    return "NOPE";
}
```

On peut voir que `getFlag()` réalise plusieurs calculs pour comparer notre input. Nous avons juste à exécuter ce même code.

```java
class Test {

  public static void main(String[] args){
      
      String str = "aaa";
      StringBuilder ace = new StringBuilder(str);
      StringBuilder jack = new StringBuilder(str);
      StringBuilder queen = new StringBuilder(str);
      StringBuilder king = new StringBuilder(str);
      ace.setCharAt(0, (char) (ace.charAt(0) + 4));
      ace.setCharAt(1, (char) (ace.charAt(1) + 19));
      ace.setCharAt(2, (char) (ace.charAt(2) + 18));
      jack.setCharAt(0, (char) (jack.charAt(0) + 7));
      jack.setCharAt(1, (char) (jack.charAt(1) + 0));
      jack.setCharAt(2, (char) (jack.charAt(2) + 1));
      queen.setCharAt(0, (char) (queen.charAt(0) + 0));
      queen.setCharAt(1, (char) (queen.charAt(1) + 11));
      queen.setCharAt(2, (char) (queen.charAt(2) + 15));
      king.setCharAt(0, (char) (king.charAt(0) + 14));
      king.setCharAt(1, (char) (king.charAt(1) + 20));
      king.setCharAt(2, (char) (king.charAt(2) + 15));
      System.out.println("".concat(queen.toString()).concat(jack.toString()).concat(ace.toString()).concat(king.toString()));
  }
}
```

```bash
$ java main.java
alphabetsoup
```

Nous devons alors fournir `alphabetsoup` comme input pour rentrer dans la condition.

Notre objectif est d'appeler la fonction `cardamom()` pour obtenir le flag.

```java
public class FlagstaffHill {
    public static native String cardamom(String str);

    public static String getFlag(String input, Context ctx) {
        return cardamom(input);
    }
}
```

Nous devons éditer le smali de la classe `FlagstaffHill` pour réaliser un appel à `cardamon(input)`, depuis `getFlag()`.

Après avoir patché notre smali, nous devons reconstruire notre apk.

```bash
# créer apk
$ java -jar ~/tools/apktool_2.4.0.jar b four_patched/ -o four_patched.apk
$ file four_patched.apk 
four_patched.apk: Zip archive data, at least v2.0 to extract

# crée clé pour signer
$ keytool -genkeypair -v -keystore key.keystore -alias publishingdoc -keyalg RSA -keysize 2048 -validity 10000

# signer
$ jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore ./key.keystore three_patched.apk publishingdoc
...
>>> Signer
    X.509, CN=a, OU=a, O=a, L=a, ST=a, C=FR
    [trusted certificate]

jar signed.

Warning: 
The signer's certificate is self-signed.
```

```bash
$ adb devices
List of devices attached
emulator-5558   device

# si besoin
$ adb uninstall com.hellocmu.picoctf 
Success
```

```bash
$ adb install four_patched.apk 
Success
```

Cela nous permet de récupérer le flag.

`picoCTF{tis.but.a.scratch}`