# -*- coding: utf-8 -*-
# Fistic Viorelia, SI-265
# Laboratorul 5 - Lucrarea A: decoderul universal

import re
import json
import base64
import argparse
import hashlib
from urllib.parse import unquote


# A2: ghicesc ce fel de codare are sirul, dupa cum arata
def ghici_strat(s):
    # intai verific url (are %), apoi hex (mai strict), apoi base64
    if "%" in s:
        return "url"
    if re.fullmatch(r"[0-9a-fA-F]+", s) and len(s) % 2 == 0:
        return "hex"
    if re.fullmatch(r"[A-Za-z0-9+/=]+", s):
        return "base64"
    return "necunoscut"


# A3: desfac stratul recunoscut mai sus
def desfa(s):
    strat = ghici_strat(s)
    if strat == "base64":
        rezultat = base64.b64decode(s)
    elif strat == "hex":
        rezultat = bytes.fromhex(s)
    elif strat == "url":
        rezultat = unquote(s).encode()
    else:
        rezultat = s.encode()
    return strat, rezultat


# verific daca toti octetii sunt caractere normale (32..126)
def citibil(b):
    for c in b:
        if c < 32 or c > 126:
            return False
    return True


# A4: decodez in bucla, cat timp mai arata ca o codare cunoscuta
# (am observat ca un strat intermediar e si el "citibil", deci
# nu ma pot opri doar cand e citibil - ma opresc cand ghici_strat
# nu mai recunoaste nimic, acolo e mesajul adevarat)
def desfa_in_bucla(s, pasi_maximi=8):
    val = s
    for _ in range(pasi_maximi):
        strat = ghici_strat(val)
        if strat == "necunoscut":
            return strat, val.encode()
        _, b = desfa(val)
        val = b.decode(errors="ignore")
    return ghici_strat(val), val.encode()


# A5: incerc toate cele 256 de chei XOR pe un octet
def sparge_xor(cale_fisier):
    date = open(cale_fisier, "rb").read()
    for k in range(256):
        clar = bytes(b ^ k for b in date)
        if citibil(clar):
            print("cheie:", k, "->", clar.decode())


# A6: caut parola unui hash intr-o wordlist
# lungimea hash-ului imi spune algoritmul: 32=md5, 40=sha1, 64=sha256
def sparge_hash(cale_hashuri, cale_wordlist):
    for linie in open(cale_hashuri):
        tinta = linie.strip()
        if not tinta:
            continue

        if len(tinta) == 32:
            algoritm = hashlib.md5
        elif len(tinta) == 40:
            algoritm = hashlib.sha1
        elif len(tinta) == 64:
            algoritm = hashlib.sha256
        else:
            print(tinta, "-> lungime necunoscuta, sar peste")
            continue

        gasit = False
        for cuv in open(cale_wordlist, encoding="latin1"):
            cuv = cuv.strip()
            if algoritm(cuv.encode()).hexdigest() == tinta:
                print(tinta, "-> parola gasita:", cuv)
                gasit = True
                break
        if not gasit:
            print(tinta, "-> nu a fost gasita in wordlist")


# A7: leg totul intr-o unealta de linie de comanda
def main():
    p = argparse.ArgumentParser(description="Decoder universal de straturi.")
    p.add_argument("intrare", help="sirul de decodat, sau o cale de fisier")
    p.add_argument("--fisier", action="store_true",
                    help="trateaza 'intrare' ca o cale catre un fisier text")
    a = p.parse_args()

    if a.fisier:
        continut = open(a.intrare, encoding="utf-8").read().strip()
    else:
        continut = a.intrare

    strat, rezultat = desfa_in_bucla(continut)

    print("strat final:", strat)
    print("rezultat:", rezultat)

    fisa = {
        "strat": strat,
        "rezultat": rezultat.decode(errors="replace"),
    }
    with open("arsenal/forensics/fisa.json", "w", encoding="utf-8") as f:
        json.dump(fisa, f, ensure_ascii=False, indent=2)
    print("fisa salvata in arsenal/forensics/fisa.json")


if __name__ == "__main__":
    main()

    # A5 si A6 le rulez separat de aici cand am nevoie:
    # sparge_xor("probe/xor.bin")
    # sparge_hash("probe/hashuri.txt", "probe/wordlist.txt")
