# forensic_250_c0rrupt

------

### Titre : c0rrupt

### Points : 250

------

### Description

------

We found this file. Recover the flag. You can also find the file in  /problems/c0rrupt_0_1fcad1344c25a122a00721e4af86de13.

#### Hints

* Try fixing the file header

------

### Résolution

---

http://www.libpng.org/pub/png/spec/1.2/PNG-Chunks.html

https://hackmd.io/@FlsYpINbRKixPQQVbh98kw/Sk_lVRCBr

https://www.w3.org/TR/2003/REC-PNG-20031110/

```bash
$ file mystery 
mystery: data
```

Le but de ce challenge va sûrement être de corriger le header de ce fichier.

```bash
$ xxd mystery
00000000: 8965 4e34 0d0a b0aa 0000 000d 4322 4452  .eN4........C"DR
00000010: 0000 066a 0000 0447 0802 0000 007c 8bab  ...j...G.....|..
00000020: 7800 0000 0173 5247 4200 aece 1ce9 0000  x....sRGB.......
00000030: 0004 6741 4d41 0000 b18f 0bfc 6105 0000  ..gAMA......a...
00000040: 0009 7048 5973 aa00 1625 0000 1625 0149  ..pHYs...%...%.I
00000050: 5224 f0aa aaff a5ab 4445 5478 5eec bd3f  R$......DETx^..?
00000060: 8e64 cd71 bd2d 8b20 2080 9041 8302 08d0  .d.q.-.  ..A....
...
```

On peut voir que les premiers octets de `mystery` sont proches de ceux d'un PNG. On peut reconnaître que `eN4` est proche de `PNG` et que `C"DR` est proche de `IHDR`. Il faut sûrement reconstituer une image au format PNG.

```bash
$ cp mystery img.png
$ hexedit img.png
```

Nous pouvons utiliser `hexedit` pour éditer notre image. Nous savons qu'une image au format PNG est divisée en plusieurs morceaux, ces morceaux sont appelés des chunks. Ces chunks contiennent des informations sur l'image en question.

```bash
$ pngcheck -v img.png
# -v: verbose
```

On peut suivre la validé de nos modifications avec `pngcheck`, ce dernier va vérifier si les chunks sont bons en utilisant le CRC-32 se trouvant à la fin de chacun d'eux. Dès que le chunk courant à le bon CRC-32, on passe au suivant, etc...

```bash
$ pngcheck -v img.png
File: test.png (202940 bytes)
  chunk IHDR at offset 0x0000c, length 13
    1642 x 1095 image, 24-bit RGB, non-interlaced
  chunk sRGB at offset 0x00025, length 1
    rendering intent = perceptual
  chunk gAMA at offset 0x00032, length 4: 0.45455
  chunk pHYs at offset 0x00042, length 9: 5669x5669 pixels/meter (144 dpi)
  chunk IDAT at offset 0x00057, length 65445
    zlib: deflated, 32K window, fast compression
  chunk IDAT at offset 0x10008, length 65524
  chunk IDAT at offset 0x20008, length 65524
  chunk IDAT at offset 0x30008, length 6304
  chunk IEND at offset 0x318b4, length 0
No errors detected in test.png (9 chunks, 96.3% compression).
$ file test.png 
test.png: PNG image data, 1642 x 1095, 8-bit/color RGB, non-interlaced
```

Étape par étape, nous nous retrouvons avec une image corrigée qui nous donne le flag.

`picoCTF{c0rrupt10n_1847995}`