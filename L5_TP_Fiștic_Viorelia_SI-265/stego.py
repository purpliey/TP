# -*- coding: utf-8 -*-
# Fistic Viorelia, SI-265
# Laboratorul 5 - Lucrarea B (partea 2): steganografie LSB

from PIL import Image


# B5: ascund mesajul in ultimul bit al fiecarui canal de culoare (R, G, B)
# salvez in .png (fara pierdere) - un .jpg ar strica bitii ascunsi
def ascunde_mesaj(cale_poza_sursa, mesaj, cale_poza_iesire="stego.png"):
    img = Image.open(cale_poza_sursa).convert("RGB")
    px = list(img.getdata())

    date_mesaj = mesaj + b"\x00"  # un octet 0 la final = sfarsitul mesajului
    biti = "".join(f"{octet:08b}" for octet in date_mesaj)

    px_nou = []
    index_bit = 0
    for (r, g, b) in px:
        canale = [r, g, b]
        for i in range(3):
            if index_bit < len(biti):
                bit = int(biti[index_bit])
                canale[i] = (canale[i] & ~1) | bit  # schimb doar ultimul bit
                index_bit += 1
        px_nou.append(tuple(canale))

    img.putdata(px_nou)
    img.save(cale_poza_iesire)
    print("mesaj ascuns in", cale_poza_iesire)


# B6: exact invers - citesc ultimul bit din fiecare canal si reconstitui mesajul
def dezvaluie_mesaj(cale_poza_stego):
    px = list(Image.open(cale_poza_stego).convert("RGB").getdata())

    biti = ""
    for (r, g, b) in px:
        biti += str(r & 1)
        biti += str(g & 1)
        biti += str(b & 1)

    octeti = bytearray()
    for i in range(0, len(biti) - 7, 8):
        octet = int(biti[i:i + 8], 2)
        if octet == 0:
            break
        octeti.append(octet)

    mesaj = bytes(octeti).decode(errors="replace")
    print("mesaj gasit:", mesaj)
    return mesaj


if __name__ == "__main__":
    ascunde_mesaj("probe/foto.jpg", b"FLAG{ascuns_in_pixeli}")
    dezvaluie_mesaj("stego.png")
