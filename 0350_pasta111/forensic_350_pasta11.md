# forensic_350_pasta111

------

### Titre : pastaAAA

### Points : 350

------

### Description

------

This pasta is up to no good. There MUST be something behind it.

#### Hints

* Try fixing the file header

------

### Résolution

---

```bash
$ file ctf.png 
ctf.png: PNG image data, 826 x 620, 8-bit/color RGB, non-interlaced
```

En utilsant `stegsolve`, nous pouvons voir que des données sont cachées sur les channels RGB, sur les bits 2-1-0.

La difficulté de ce challenge est de trouver les bons caractères de celui-ci, notamment, le `$`.

`picoCTF{pa$ta_1s_lyf3}`