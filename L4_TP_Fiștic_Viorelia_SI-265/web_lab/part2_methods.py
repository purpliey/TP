# Laborator: funcții, metode și importuri pe web
# Student: Fiștic Viorelia

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

import time
import requests



# Exercițiul 9. Elementele de bază ale răspunsului

response = requests.get(BASE_URL, timeout=TIMEOUT)

print("status_code:", response.status_code)  # atribut
print("ok:", response.ok)                    # atribut (proprietate)
print("url:", response.url)                  # atribut
print("encoding:", response.encoding)        # atribut


# Exercițiul 10. Tratarea erorilor cu o metodă

print("\n--- Ex. 10 ---")
response.raise_for_status()  # nu face nimic dacă totul e în regulă (2xx)

print("Pagina principală: fără erori.")

time.sleep(1)
try:
    r404 = requests.get(BASE_URL + "/this-page-does-not-exist", timeout=TIMEOUT)
    r404.raise_for_status()
    
except requests.HTTPError as err:
    print("Pagina cerută nu există sau serverul a răspuns cu eroare:", err)


# Exercițiul 11. Toate antetele

print("\n--- Ex. 11 ---")
for nume, valoare in response.headers.items():
    print(f"{nume}: {valoare}")


# Exercițiul 12. Metode de dicționar


print("\n--- Ex. 12 ---")
print("Server:", response.headers.get("Server", "lipsește"))

print("Content-Type:", response.headers.get("Content-Type", "lipsește"))
print("content-type (litere mici):", response.headers.get("content-type", "lipsește"))
# Observație: se obține aceeași valoare. response.headers este un
# CaseInsensitiveDict: numele antetelor nu țin cont de majuscule/minuscule
# (conform HTTP), spre deosebire de un dicționar obișnuit.


# Exercițiul 13. Înlănțuirea metodelor de șir


print("\n--- Ex. 13 ---")
print("Apariții 'cyber':", response.text.lower().count("cyber"))
# Putem înlănțui pentru că .lower() returnează un șir nou (str), iar orice
# str are metoda .count(). Rezultatul fiecărei metode este obiectul pe care
# se apelează următoarea.


# Exercițiul 14. Găsirea titlului


print("\n--- Ex. 14 ---")
html = response.text
start = html.find("<title>") + len("<title>")
end = html.find("</title>")

print("Titlu:", html[start:end].strip())


# Exercițiul 15. Numărarea liniilor

print("\n--- Ex. 15 ---")
lines = html.splitlines()
print("Număr de linii:", len(lines))
print("Lungimea celei mai lungi linii:", len(max(lines, key=len)))


# Exercițiul 16. Verificarea HTTPS

print("\n--- Ex. 16 ---")
if response.url.startswith("https://"):
    print("Conexiune securizată")
else:
    print("Conexiune nesecurizată")


# Exercițiul 17. Urmărirea redirecționărilor

print("\n--- Ex. 17 ---")
time.sleep(1)

r = requests.get("http://cybercor.org", timeout=TIMEOUT)
for pas in r.history:
    
    print(pas.status_code, pas.url)
print("URL final:", r.url)


# Exercițiul 18. HEAD versus GET

print("\n--- Ex. 18 ---")
time.sleep(1)


r_head = requests.head(BASE_URL, timeout=TIMEOUT)
time.sleep(1)

r_get = requests.get(BASE_URL, timeout=TIMEOUT)
print("HEAD, len(content):", len(r_head.content))
print("GET,  len(content):", len(r_get.content))
# HEAD returnează doar antetele, fără corp, deci len(content) este 0.
# GET returnează și corpul (pagina HTML), deci len(content) este mare.


# Exercițiul 19. Cookie-uri

print("\n--- Ex. 19 ---")
if len(response.cookies) == 0:
    print("Niciun cookie setat")
else:
    for cookie in response.cookies:
        print(cookie.name, cookie.secure)


# Exercițiul 20. Sesiuni

print("\n--- Ex. 20 ---")
time.sleep(1)
session = requests.Session()
session.headers.update({"User-Agent": "WebLab-NumePrenume"})
r = session.get(ECHO_URL + "/headers", timeout=TIMEOUT)  # către httpbin, nu cybercor
trimis = r.json()["headers"].get("User-Agent")
print("User-Agent primit de server:", trimis)
print("Antetul a fost trimis:", trimis == "WebLab-NumePrenume")


# Verificați-vă: response.text vs response.json()

# response.text este un atribut (proprietate): o valoare deja disponibilă
#   (corpul decodat), deci se citește fără paranteze.
# response.json() este o metodă: execută o acțiune (parsează corpul ca JSON,
#   poate ridica eroare dacă nu e JSON valid), deci se apelează cu paranteze.
