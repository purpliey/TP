# -*- coding: utf-8 -*-
# Fistic Viorelia, SI-265
# Laboratorul 5 - Lucrarea B (partea 1): forensics pe fisiere

import re
from PIL import Image
from PIL.ExifTags import TAGS


# B1: tipul real al fisierului, dupa primii octeti (nu dupa extensie)
def tip_real(cale):
    cap = open(cale, "rb").read(8)
    if cap.startswith(b"%PDF"):
        return "pdf"
    if cap.startswith(b"\x89PNG"):
        return "png"
    if cap.startswith(b"\xff\xd8"):
        return "jpeg"
    if cap.startswith(b"PK\x03\x04"):
        return "zip/docx"
    return "necunoscut (" + cap.hex() + ")"


# B2: scot sirurile de caractere imprimabile dintr-un fisier binar
def extrage_text(cale):
    date = open(cale, "rb").read()
    gasite = re.findall(rb"[ -~]{4,}", date)
    for m in gasite:
        print(m.decode())
    return gasite


# transform (grade, minute, secunde) in grade zecimale
# PIL citeste aceste numere ca fractii (IFDRational), nu ca float,
# asa ca le transform explicit cu float(), altfel suma iese gresita
def grade_zecimale(valoare, emisfera):
    grade, minute, secunde = valoare
    grade, minute, secunde = float(grade), float(minute), float(secunde)
    rezultat = grade + minute / 60 + secunde / 3600
    if emisfera in ("S", "W"):
        rezultat = -rezultat
    return rezultat


# B3: citesc EXIF-ul unei poze si scot coordonatele GPS
def citeste_exif_gps(cale):
    exif = Image.open(cale)._getexif() or {}
    for id, val in exif.items():
        print(TAGS.get(id, id), "=", val)

    gps = exif.get(34853)  # 34853 = tag-ul blocului GPS
    if gps:
        lat = grade_zecimale(gps[2], gps[1])
        lon = grade_zecimale(gps[4], gps[3])
        print("Latitudine:", lat)
        print("Longitudine:", lon)


# B4: caut o semnatura (de obicei zip) lipita la coada fisierului
def extrage_fisier_ascuns(cale, semnatura=b"PK\x03\x04", nume_iesire="gasit.zip"):
    date = open(cale, "rb").read()
    i = date.find(semnatura)
    if i == -1:
        print("nu s-a gasit nicio semnatura ascunsa")
        return None

    with open(nume_iesire, "wb") as f:
        f.write(date[i:])
    print("arhiva extrasa de la octetul", i, "in", nume_iesire)
    return nume_iesire


if __name__ == "__main__":
    print("--- B1: tip real ---")
    print(tip_real("probe/foto.jpg"))

    print("\n--- B2: text ascuns in ascuns.png ---")
    extrage_text("probe/ascuns.png")

    print("\n--- B3: EXIF si GPS din foto.jpg ---")
    citeste_exif_gps("probe/foto.jpg")

    print("\n--- B4: file carving din ascuns.png ---")
    extrage_fisier_ascuns("probe/ascuns.png")
