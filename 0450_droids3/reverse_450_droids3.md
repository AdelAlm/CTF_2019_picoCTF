# reverse_450_droids3

------

### Titre : droids3

### Points : 450

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
$ file three.apk 
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
public static native String cilantro(String str);

public static String nope(String input) {
    return "don't wanna";
}

public static String yep(String input) {
	return cilantro(input);
}

public static String getFlag(String input, Context ctx) {
	return nope(input);
}
```

On peut voir que `getFlag()` appelle `nope(input)`, alors que nous voulons appeler `yep(input)`. Nous allons essayer de patcher notre `apkt` en éditant le code smali.

```bash
$ cp -r three three_patched
# avant
$ cat three/smali/com/hellocmu/picoctf/FlagstaffHill.smali
.method public static getFlag(Ljava/lang/String;Landroid/content/Context;)Ljava/lang/String;                                                    
.locals 1                                                                                                                                   
.param p0, "input"    # Ljava/lang/String;                                                                                                  
.param p1, "ctx"    # Landroid/content/Context;                                                                                             

.line 19                                                                                                                                    
invoke-static {p0}, Lcom/hellocmu/picoctf/FlagstaffHill;->nope(Ljava/lang/String;)Ljava/lang/String;                                        

move-result-object v0

.line 20
.local v0, "flag":Ljava/lang/String;
return-object v0
.end method

# après
$ cat three_patched/smali/com/hellocmu/picoctf/FlagstaffHill.smali
.method public static getFlag(Ljava/lang/String;Landroid/content/Context;)Ljava/lang/String;
.locals 1
.param p0, "input"    # Ljava/lang/String;
.param p1, "ctx"    # Landroid/content/Context;

.line 19
invoke-static {p0}, Lcom/hellocmu/picoctf/FlagstaffHill;->yep(Ljava/lang/String;)Ljava/lang/String; # on change ici

move-result-object v0

.line 20
.local v0, "flag":Ljava/lang/String;
return-object v0
.end method
```

```bash
# avant
>nope(Ljava/lang/String;)Ljava/lang/String;   
# après
>yep(Ljava/lang/String;)Ljava/lang/String;
```

Nous avons patcher notre smali. nous devons maintenant reconstituer notre apk.

```bash
# créer apk
$ java -jar ~/tools/apktool_2.4.0.jar b three_patched/ -o three_patched.apk
$ file three_patched.apk 
three_patched.apk: Zip archive data, at least v2.0 to extract

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
$ adb install three_patched.apk 
Success
```

Cela nous permet de récupérer le flag.

`picoCTF{tis.but.a.scratch}`