# crypto_400_aes_abc

------

### Titre : AES-ABC

### Points : 400

------

### Description

------

AES-ECB is bad, so I rolled my own cipher block chaining mechanism - Addition Block Chaining! You can find the source here: aes-abc.py. The AES-ABC flag is body.enc.ppm

#### Hints

* You probably want to figure out what the flag looks like in ECB form...

------

### Résolution

---

```bash
$ file body.enc.ppm 
body.enc.ppm: Netpbm image data, size = 1895 x 820, rawbits, pixmap
```

Dans `aes-abc.py`, c'est le chiffrement AES-ECB qui est utilisé.

> The simplest of the encryption modes is the Electronic Codebook (ECB) mode (named after conventional physical codebooks). The message is divided into blocks, and each block is encrypted separately.  (Wikipedia)

Le mode ECB est facile à attaquer.

```python
# aes-abc.py
def aes_abc_encrypt(pt):
    cipher = AES.new(KEY, AES.MODE_ECB)
    ct = cipher.encrypt(pad(pt))

    blocks = [ct[i * BLOCK_SIZE:(i+1) * BLOCK_SIZE] for i in range(len(ct) / BLOCK_SIZE)]
    iv = os.urandom(16)
    blocks.insert(0, iv)
    
    for i in range(len(blocks) - 1):
        prev_blk = int(blocks[i].encode('hex'), 16)
        curr_blk = int(blocks[i+1].encode('hex'), 16)

        n_curr_blk = (prev_blk + curr_blk) % UMAX
        blocks[i+1] = to_bytes(n_curr_blk)

    ct_abc = "".join(blocks)
 
    return iv, ct_abc, ct
```

```python
# aes-abc_patched.py
def aes_abc_encrypt(pt):
    ct = pad(pt)

    blocks = [ct[i * BLOCK_SIZE:(i+1) * BLOCK_SIZE] for i in range(len(ct) / BLOCK_SIZE)]
    iv = os.urandom(16)
    blocks.insert(0, iv)
    
    test = list(blocks)
    for i in range(len(blocks) - 1):
        prev_blk = int(test[i].encode('hex'), 16)
        curr_blk = int(blocks[i+1].encode('hex'), 16)

        n_curr_blk = (curr_blk - prev_blk) % UMAX
        blocks[i+1] = to_bytes(n_curr_blk)

    ct_abc = "".join(blocks)
 
    return iv, ct_abc, ct

if __name__=="__main__":
    with open('body.enc.ppm', 'rb') as f:
        header, data = parse_header_ppm(f)
    
    iv, c_img, ct = aes_abc_encrypt(data)

    with open('body.dec.ppm', 'wb') as fw:
        fw.write(header)
        fw.write(c_img)
```

On doit juste comprendre le chiffrement et inverser le chiffrement pour déchiffrer. On exécute et on peut voir le flag sur l'image.

`picoCTF{d0Nt_r0ll_yoUr_0wN_aES}`